#!/usr/bin/env python3
"""
Inference test for yolo26-seg on Hailo-8.
Full pipeline: Hailo inference -> mask -> BEV -> sliding windows -> CTE

Usage:
    python3 test_yolo26_hailo.py image <image.jpg> [hef] [threshold]
    python3 test_yolo26_hailo.py camera            [hef] [threshold]

Examples:
    python3 test_yolo26_hailo.py image test.jpg
    python3 test_yolo26_hailo.py camera
    python3 test_yolo26_hailo.py camera yolo26n_seg_640.hef 0.3

Image mode:  saves result_<name>.jpg
Camera mode: display via GStreamer/waylandsink, Ctrl+C to stop
"""

import sys
import os
import subprocess
import time
import cv2
import numpy as np
from dataclasses import dataclass
from typing import Optional, Tuple
def _read_cpu_stat():
    """Reads /proc/stat and returns (user, system, idle, total) in jiffies."""
    r = open("/proc/stat").readline().split()
    user   = int(r[1]) + int(r[2])  # user + nice
    system = int(r[3])
    idle   = int(r[4])
    total  = sum(int(x) for x in r[1:])
    return user, system, idle, total

_cpu_stat_prev = _read_cpu_stat()

def _read_temp():
    try:
        with open("/sys/class/thermal/thermal_zone0/temp") as f:
            return int(f.read().strip()) / 1000.0
    except Exception:
        return 0.0

from hailo_platform import (
    ConfigureParams,
    HEF,
    HailoStreamInterface,
    InferVStreams,
    InputVStreamParams,
    OutputVStreamParams,
    FormatType,
    VDevice,
)

# ---------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------
args       = sys.argv[1:]
NO_DISPLAY = "--no-display" in args
REMOTE     = "--remote" in args
args       = [a for a in args if a not in ("--no-display", "--remote")]

MODE = args[0] if args else "image"

if MODE == "camera":
    HEF_PATH        = args[1] if len(args) > 1 else "yolo26n_seg_640.hef"
    SCORE_THRESHOLD = float(args[2]) if len(args) > 2 else 0.25
    IMAGE_PATH      = None
elif MODE == "image":
    IMAGE_PATH      = args[1] if len(args) > 1 else None
    HEF_PATH        = args[2] if len(args) > 2 else "yolo26n_seg_640.hef"
    SCORE_THRESHOLD = float(args[3]) if len(args) > 3 else 0.25
else:
    print(__doc__)
    sys.exit(1)

MODEL_NAME = os.path.splitext(os.path.basename(HEF_PATH))[0]

# Maximum NPU FPS in hw_only mode (measured with hailortcli benchmark)
_HEF_MAX_FPS = {
    "yolo26n_seg_640": 68.72,
    "yolo26s_seg_640": 33.24,
}
MODEL_MAX_HW_FPS = _HEF_MAX_FPS.get(MODEL_NAME, None)

# NET_SIZE and PROTO_SIZE are auto-detected from HEF in main()
NET_SIZE     = None
PROTO_SIZE   = None
NUM_CHANNELS = None  # 37 (s/1class) or 38 (n/2class), auto-detected from output
TOP_K        = 200
CAM_WIDTH    = 640
CAM_HEIGHT   = 360
CAM_FPS      = 30
DISPLAY_WIDTH  = 1260
DISPLAY_HEIGHT = 400

# ---------------------------------------------------------------
# Pre-processing
# ---------------------------------------------------------------
def preprocess(img_bgr, net_size):
    img_rgb = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2RGB)
    img_resized = cv2.resize(img_rgb, (net_size, net_size))
    return np.expand_dims(img_resized, axis=0).astype(np.uint8)

# ---------------------------------------------------------------
# Output key discovery by shape (executed once)
# Suporta dois modos:
#   - 4 outputs: det[1,C,8400] + proto[1,32,H,H]  (Concat_4 cut)
#   - 10 outputs: cv2.x[1,4,H,W] + cv3.x[1,1,H,W] + cv4.x[1,32,H,W] + proto (per-scale cut)
# ---------------------------------------------------------------
_output_keys  = {}
_output_mode  = None  # "concat4", "per_scale" or "pre_concat4"

def find_output_keys(outputs):
    global _output_keys, _output_mode, NUM_CHANNELS
    if _output_keys:
        return _output_keys

    print("\n[outputs received from Hailo]")
    for name, val in outputs.items():
        print(f"  {name}: shape={val.shape} dtype={val.dtype}")

    # Detect proto: tensor with 32 channels and SQUARE spatial dims (HxH)
    # Ex: (1,160,160,32) or (1,32,160,160) — distinguishes from mask_coef (1,1,8400,32)
    proto_candidate = None
    for name, val in outputs.items():
        s = val.shape
        if len(s) == 4 and 32 in s:
            spatial_dims = [d for d in s if d != 1 and d != 32]
            # Proto has two equal spatial dims (square): e.g. 160,160
            if len(spatial_dims) >= 2 and spatial_dims[0] == spatial_dims[1]:
                proto_candidate = name
                break
            # Fallback: proto is the only 32ch tensor with dims < 8400
            elif len(spatial_dims) == 1 and spatial_dims[0] < 1000:
                proto_candidate = name

    if proto_candidate:
        _output_keys["proto"] = proto_candidate
        print(f"  -> proto: {proto_candidate} shape={outputs[proto_candidate].shape}")

    non_proto = {n: v for n, v in outputs.items() if n != proto_candidate}

    # Try to detect pre_concat4 mode: tensors with 8400 in shape (concat of 3 scales)
    # Ex: ew_mult1(1,1,8400,4), activation3(1,1,8400,1), concat22(1,1,8400,32)
    pre_concat4_bbox  = None
    pre_concat4_score = None
    pre_concat4_mask  = None

    for name, val in non_proto.items():
        s = val.shape
        if 8400 not in s:
            continue
        if 4 in s:
            pre_concat4_bbox = name
        elif 1 in s and max(d for d in s if d != 8400) <= 1:
            pre_concat4_score = name
        elif 32 in s:
            pre_concat4_mask = name

    if pre_concat4_bbox and pre_concat4_score and pre_concat4_mask:
        _output_mode = "pre_concat4"
        _output_keys["bbox"]  = pre_concat4_bbox
        _output_keys["score"] = pre_concat4_score
        _output_keys["mask"]  = pre_concat4_mask
        NUM_CHANNELS = 4 + 1 + 32
        print(f"  -> mode: pre_concat4 (3 concatenated outputs)")
        print(f"     bbox:  {pre_concat4_bbox} {outputs[pre_concat4_bbox].shape}")
        print(f"     score: {pre_concat4_score} {outputs[pre_concat4_score].shape}")
        print(f"     mask:  {pre_concat4_mask} {outputs[pre_concat4_mask].shape}")
        return _output_keys

    # Try to detect per_scale mode (10 outputs)
    bbox_scales  = {}
    score_scales = {}
    mask_scales  = {}

    for name, val in non_proto.items():
        s = val.shape
        if len(s) != 4:
            continue
        if 4 in s:
            h = max(d for d in s if d not in (1, 4))
            bbox_scales[h] = name
        elif all(d in (1, 20, 40, 80) for d in s):
            h = max(s)
            score_scales[h] = name
        elif 32 in s:
            h = max(d for d in s if d not in (1, 32))
            mask_scales[h] = name

    if bbox_scales and score_scales and mask_scales:
        _output_mode = "per_scale"
        _output_keys["bbox_scales"]  = bbox_scales
        _output_keys["score_scales"] = score_scales
        _output_keys["mask_scales"]  = mask_scales
        NUM_CHANNELS = 4 + 1 + 32
        print(f"  -> mode: per_scale (10 outputs)")
        print(f"     bbox:  {bbox_scales}")
        print(f"     score: {score_scales}")
        print(f"     mask:  {mask_scales}")
    else:
        # Fallback: modo concat4
        _output_mode = "concat4"
        for name, val in non_proto.items():
            s = val.shape
            if any(d >= 37 and d <= 40 for d in s):
                _output_keys["det"] = name
                NUM_CHANNELS = [d for d in s if 37 <= d <= 40][0]
                print(f"  -> mode: concat4  det={name} channels={NUM_CHANNELS}")
                break

    return _output_keys

# ---------------------------------------------------------------
# YOLO26-seg post-processing -> binary mask 0/255
# ---------------------------------------------------------------
def yolo26_to_mask(outputs, orig_h, orig_w, score_threshold, top_k):
    """
    Converts Hailo outputs to a binary mask uint8 (0/255).
    Supports:
      - concat4 mode:     det[1,C,8400] + proto[1,32,H,H]
      - per_scale mode:   cv2.x + cv3.x + cv4.x per scale + proto  (10 outputs)
      - pre_concat4 mode: bbox + score + mask_coef (concatenated 8400) + proto  (3 outputs)
    """
    keys = find_output_keys(outputs)
    if "proto" not in keys:
        return np.zeros((orig_h, orig_w), dtype=np.uint8)

    proto_raw = outputs[keys["proto"]]

    if _output_mode == "pre_concat4":
        # Tensors arrive in NHWC with 8400 as spatial dim: (1,1,8400,C)
        def squeeze_8400(name):
            t = outputs[name].astype(np.float32)  # (1,1,8400,C) ou (1,C,8400,1)
            return t.reshape(8400, -1)             # (8400, C)

        bbox_t  = squeeze_8400(keys["bbox"])   # (8400, 4)
        score_t = squeeze_8400(keys["score"])  # (8400, 1)
        mask_t  = squeeze_8400(keys["mask"])   # (8400, 32)

        scores      = score_t.squeeze(1)  # (8400,)
        mask_coeffs = mask_t              # (8400, 32)
        det = np.concatenate([bbox_t, score_t, mask_t], axis=1)  # (8400, 37) para debug

    elif _output_mode == "per_scale":
        # Tensors arrive in NHWC (1,H,W,C) — transpose to NCHW before flatten
        def concat_scales(scale_dict):
            tensors = []
            for h in sorted(scale_dict.keys(), reverse=True):  # 80, 40, 20
                t = outputs[scale_dict[h]].astype(np.float32)  # (1,H,W,C)
                t = np.transpose(t, (0, 3, 1, 2))              # (1,C,H,W)
                tensors.append(t.reshape(1, t.shape[1], -1))   # (1,C,H*W)
            return np.concatenate(tensors, axis=2)              # (1,C,8400)

        score     = concat_scales(keys["score_scales"])  # [1,1,8400]
        mask_coef = concat_scales(keys["mask_scales"])   # [1,32,8400]

        scores      = score.squeeze()          # [8400]
        mask_coeffs = mask_coef.squeeze(0).T  # [8400,32]

        if not hasattr(yolo26_to_mask, '_printed_scores'):
            bbox = concat_scales(keys["bbox_scales"])
            det  = np.concatenate([bbox, score, mask_coef], axis=1).squeeze(0).T
        else:
            det = None

    else:
        # Modo concat4
        if "det" not in keys:
            return np.zeros((orig_h, orig_w), dtype=np.uint8)
        det_raw = outputs[keys["det"]]
        det = det_raw.squeeze().astype(np.float32)
        if NUM_CHANNELS and det.shape[0] == NUM_CHANNELS:
            det = det.T
        nc = det.shape[1] - 4 - 32
        scores      = det[:, 4:4+nc].max(axis=1)
        mask_coeffs = det[:, 4+nc:]

    # Fallback: if scores have no variance (zero-point), use coefficient norms
    if scores.max() - scores.min() < 0.01:
        scores = np.linalg.norm(mask_coeffs, axis=1).astype(np.float32)
        scores = (scores - scores.min()) / (scores.max() - scores.min() + 1e-6)

    # Proto: (1,104,104,32) -> (32,104,104)
    proto = proto_raw.squeeze(0).astype(np.float32)
    if proto.shape[-1] == 32:
        proto = np.transpose(proto, (2, 0, 1))

    # Top-K
    n_candidates = min(top_k, len(scores))
    top_idx     = np.argpartition(scores, -n_candidates)[-n_candidates:]
    top_scores  = scores[top_idx]
    top_coeffs  = mask_coeffs[top_idx]

    # Full tensor debug (printed once)
    if not hasattr(yolo26_to_mask, '_printed_scores'):
        yolo26_to_mask._printed_scores = True
        print(f"[SCORES] min={scores.min():.4f}  max={scores.max():.4f}  mean={scores.mean():.4f}  mode={_output_mode}")
        if det is not None:
            print(f"[DET] shape={det.shape}")
            for i in range(det.shape[1]):
                print(f"  ch{i:02d}: min={det[:,i].min():.4f}  max={det[:,i].max():.4f}")

    valid = top_scores > score_threshold
    if not np.any(valid):
        return np.zeros((orig_h, orig_w), dtype=np.uint8)

    valid_scores = top_scores[valid]
    valid_coeffs = top_coeffs[valid]

    P = proto.shape[1]
    proto_flat = proto.reshape(32, -1)

    raw_masks = valid_coeffs @ proto_flat                              # (V, P*P)
    raw_masks = 1.0 / (1.0 + np.exp(-np.clip(raw_masks, -20, 20)))   # sigmoid
    raw_masks = raw_masks.reshape(len(valid_scores), P, P)

    weights  = valid_scores / np.maximum(valid_scores.sum(), 1e-6)
    combined = (weights[:, None, None] * raw_masks).sum(axis=0)       # (P, P)

    mask_resized = cv2.resize(combined, (orig_w, orig_h))

    # Adaptive threshold: mean + 0.1*std, minimum 0.3
    thr = max(float(mask_resized.mean() + 0.1 * mask_resized.std()), 0.3)
    _, binary = cv2.threshold(mask_resized, thr, 255, cv2.THRESH_BINARY)
    return binary.astype(np.uint8)

# ---------------------------------------------------------------
# Mask Post-Processor (morphology)
# ---------------------------------------------------------------
class MaskPostProcessor:
    def __init__(self, close_kernel=(5, 15), open_kernel=(5, 5)):
        self.close_k = cv2.getStructuringElement(cv2.MORPH_RECT, close_kernel)
        self.open_k  = cv2.getStructuringElement(cv2.MORPH_RECT, open_kernel)

    def process(self, mask):
        closed = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, self.close_k)
        return cv2.morphologyEx(closed, cv2.MORPH_OPEN, self.open_k)

# ---------------------------------------------------------------
# BEV Transform
# ---------------------------------------------------------------
class BEVTransform:
    DEFAULT_SRC = np.float32([
        [0.255, 0.44], [0.745, 0.44],  # top-left, top-right
        [1.17, 1.00], [-0.17, 1.00]  # bottom-right, bottom-left
    ])
    DEFAULT_DST = np.float32([
        [0.25, 0.00], [0.75, 0.00],
        [0.75, 1.00], [0.25, 1.00]
    ])

    def __init__(self, w, h, src=None, dst=None):
        self.w, self.h = w, h
        src = src if src is not None else self.DEFAULT_SRC
        dst = dst if dst is not None else self.DEFAULT_DST
        src_px = (src * np.array([w, h], dtype=np.float32)).astype(np.float32)
        dst_px = (dst * np.array([w, h], dtype=np.float32)).astype(np.float32)
        self.M     = cv2.getPerspectiveTransform(src_px, dst_px)
        self.M_inv = cv2.getPerspectiveTransform(dst_px, src_px)

    def warp(self, img):
        return cv2.warpPerspective(img, self.M, (self.w, self.h))

    def unwarp(self, img):
        return cv2.warpPerspective(img, self.M_inv, (self.w, self.h))

# ---------------------------------------------------------------
# Sliding Windows + Polyfit
# ---------------------------------------------------------------
@dataclass
class LaneFitResult:
    left_fit:         Optional[np.ndarray]
    right_fit:        Optional[np.ndarray]
    cte_pixels:       Optional[float]
    cte_meters:       Optional[float]
    curvature_meters: Optional[float]
    left_found:       bool
    right_found:      bool

class SlidingWindowsLaneFitter:
    def __init__(self, n_windows=9, margin=80, min_pixels=50, lane_width_meters=3.7):
        self.n_windows         = n_windows
        self.margin            = margin
        self.min_pixels        = min_pixels
        self.lane_width_meters = lane_width_meters
        self._ppm_x            = None
        self._prev_left        = None
        self._prev_right       = None

    def fit(self, bev_mask):
        h, w = bev_mask.shape[:2]
        left_base, right_base = self._histogram_peaks(bev_mask)
        left_px, right_px = self._sliding_windows(bev_mask, left_base, right_base, h, w)
        left_fit  = self._polyfit(left_px)
        right_fit = self._polyfit(right_px)

        if self._ppm_x is None and left_fit is not None and right_fit is not None:
            self._calibrate(left_fit, right_fit, h)

        cte_px, cte_m = self._cte(left_fit, right_fit, w, h)
        curve = self._curvature(left_fit, h) if left_fit is not None else 0.0

        left_fit  = self._smooth(left_fit,  self._prev_left)
        right_fit = self._smooth(right_fit, self._prev_right)
        self._prev_left  = left_fit
        self._prev_right = right_fit

        return LaneFitResult(
            left_fit=left_fit, right_fit=right_fit,
            cte_pixels=cte_px, cte_meters=cte_m,
            curvature_meters=curve,
            left_found=left_fit is not None,
            right_found=right_fit is not None,
        )

    def _histogram_peaks(self, mask):
        h, w = mask.shape[:2]
        hist = np.sum(mask[h // 2:, :], axis=0)
        mid  = w // 2
        mg   = int(w * 0.15)
        ls   = hist[mg:mid]
        rs   = hist[mid:w - mg]
        lb   = int(np.argmax(ls)) + mg if ls.max() > 0 else int(w * 0.25)
        rb   = int(np.argmax(rs)) + mid if rs.max() > 0 else int(w * 0.75)
        return lb, rb

    def _sliding_windows(self, mask, left_base, right_base, h, w):
        win_h     = h // self.n_windows
        nz        = mask.nonzero()
        nz_y      = np.array(nz[0])
        nz_x      = np.array(nz[1])
        lc, rc    = left_base, right_base
        l_inds, r_inds = [], []

        for win in range(self.n_windows):
            y_lo = h - (win + 1) * win_h
            y_hi = h - win * win_h
            gl = ((nz_y >= y_lo) & (nz_y < y_hi) &
                  (nz_x >= lc - self.margin) & (nz_x < lc + self.margin)).nonzero()[0]
            gr = ((nz_y >= y_lo) & (nz_y < y_hi) &
                  (nz_x >= rc - self.margin) & (nz_x < rc + self.margin)).nonzero()[0]
            l_inds.append(gl)
            r_inds.append(gr)
            if len(gl) > self.min_pixels: lc = int(np.mean(nz_x[gl]))
            if len(gr) > self.min_pixels: rc = int(np.mean(nz_x[gr]))

        li = np.concatenate(l_inds)
        ri = np.concatenate(r_inds)
        return (nz_x[li], nz_y[li]), (nz_x[ri], nz_y[ri])

    def _polyfit(self, px):
        x, y = px
        if len(x) < 100:
            return None
        try:
            return np.polyfit(y, x, 2)
        except np.RankWarning:
            return None

    def _calibrate(self, lf, rf, h):
        y = h - 1
        lx = lf[0]*y**2 + lf[1]*y + lf[2]
        rx = rf[0]*y**2 + rf[1]*y + rf[2]
        wpx = abs(rx - lx)
        if wpx > 0:
            self._ppm_x = wpx / self.lane_width_meters

    def _cte(self, lf, rf, w, h):
        y    = h - 1
        vc   = w / 2.0
        if lf is not None and rf is not None:
            lx = lf[0]*y**2 + lf[1]*y + lf[2]
            rx = rf[0]*y**2 + rf[1]*y + rf[2]
            lc = (lx + rx) / 2.0
        elif lf is not None:
            lx = lf[0]*y**2 + lf[1]*y + lf[2]
            lc = lx + (self._ppm_x * self.lane_width_meters / 2.0 if self._ppm_x else w * 0.25)
        elif rf is not None:
            rx = rf[0]*y**2 + rf[1]*y + rf[2]
            lc = rx - (self._ppm_x * self.lane_width_meters / 2.0 if self._ppm_x else w * 0.25)
        else:
            return None, None
        cte_px = vc - lc
        cte_m  = cte_px / self._ppm_x if self._ppm_x else None
        return cte_px, cte_m

    def _curvature(self, fit, y):
        if fit is None or self._ppm_x is None:
            return 0.0
        mx = my = self._ppm_x
        a, b, _ = fit
        num = (1 + (2*a*y*mx/(my**2) + b*mx/my)**2)**1.5
        den = abs(2*a*mx/(my**2))
        return num / den if den > 0 else 0.0

    def _smooth(self, cur, prev, alpha=0.25):
        if cur is None:  return prev
        if prev is None: return cur
        return alpha * cur + (1.0 - alpha) * prev

# ---------------------------------------------------------------
# Visualization
# ---------------------------------------------------------------
def draw_lane_overlay(frame_bgr, fit: LaneFitResult, bev: BEVTransform):
    """Draws lane geometry (lanes, trapezoid) at original resolution."""
    h, w   = frame_bgr.shape[:2]
    result = frame_bgr.copy()
    y_vals = np.arange(0, h)

    def poly_pts(f):
        x = f[0]*y_vals**2 + f[1]*y_vals + f[2]
        x = np.clip(x, 0, w - 1)
        return np.stack([x, y_vals], axis=1).astype(np.int32)

    if fit.left_found or fit.right_found:
        overlay = np.zeros_like(frame_bgr)
        lp = poly_pts(fit.left_fit)  if fit.left_found  else None
        rp = poly_pts(fit.right_fit) if fit.right_found else None

        if lp is not None and rp is not None:
            pts = np.vstack([lp, rp[::-1]])
            cv2.fillPoly(overlay, [pts], (0, 150, 0))
            cx = (lp[:, 0] + rp[:, 0]) / 2
            cp = np.stack([cx, y_vals], axis=1).astype(np.int32)
            cv2.polylines(overlay, [cp], False, (0, 255, 255), 1)

        if lp is not None: cv2.polylines(overlay, [lp], False, (255, 0, 0), 10)
        if rp is not None: cv2.polylines(overlay, [rp], False, (0, 0, 255), 10)

        unwarped = bev.unwarp(overlay)
        result   = cv2.addWeighted(result, 1.0, unwarped, 0.4, 0)

        # BEV trapezoid
        src_pts = (BEVTransform.DEFAULT_SRC * [w, h]).astype(np.int32)
        cv2.polylines(result, [src_pts], True, (255, 0, 255), 1)

    return result


def draw_text_overlay(frame, fit: LaneFitResult, inf_ms, fps=None, cpu_ms=None,
                      temp=None, model_name=None, cpu_used=None, cpu_free=None):
    """Draws text overlays on the frame already resized for display."""
    h, w = frame.shape[:2]
    result = frame

    def put(txt, pos, color, scale=0.8, thick=2):
        cv2.putText(result, txt, pos, cv2.FONT_HERSHEY_SIMPLEX, scale, color, thick)

    # Curvature
    if fit.left_found or fit.right_found:
        if fit.curvature_meters is not None:
            a = fit.left_fit[0] if fit.left_found else (fit.right_fit[0] if fit.right_found else 0)
            if fit.curvature_meters > 3000:
                ctxt = "Straight"
            elif a > 0.0001:
                ctxt = f"Right ({fit.curvature_meters:.0f}m)"
            elif a < -0.0001:
                ctxt = f"Left ({fit.curvature_meters:.0f}m)"
            else:
                ctxt = "Straight"
            put(ctxt, (20, 80), (0, 0, 0))
    else:
        put("NO LANES", (w//2 - 80, h//2), (0, 0, 0), scale=1.2, thick=3)

    # CTE
    if fit.cte_meters is not None:
        cte_txt = f"CTE: {fit.cte_meters:+.3f} m"
    else:
        cte_txt = "CTE: calibrating..."
    put(cte_txt, (20, 40), (0, 0, 0))

    # CTE bar
    bm = w // 2
    cv2.line(result, (bm - 100, 58), (bm + 100, 58), (255, 255, 0), 1)
    if fit.cte_pixels is not None:
        dx = int(bm - fit.cte_pixels * 0.2)
        cv2.circle(result, (np.clip(dx, bm-100, bm+100), 58), 7, (255, 255, 0), -1)

    # Model name (top right)
    if model_name:
        put(model_name, (w - 10 - len(model_name) * 9, 20), (200, 200, 200), scale=0.5, thick=1)

    # Line 1: latencies + NPU% + temp
    label = f"Hailo: {inf_ms:.1f}ms" + (f"  FPS: {fps:.1f}" if fps else "")
    if fps and MODEL_MAX_HW_FPS:
        npu_util = min(100, fps / MODEL_MAX_HW_FPS * 100 * 0.95)
        label += f"  NPU: {npu_util:.0f}%"
    if cpu_ms is not None:
        label += f"  Post: {cpu_ms:.1f}ms"
    if temp is not None:
        label += f"  Temp: {temp:.0f}C"
    put(label, (10, h - 35), (0, 0, 0), scale=0.65)

    # Line 2: CPU used / free
    if cpu_used is not None and cpu_free is not None:
        put(f"CPU: {cpu_used:.0f}% used  free: {cpu_free:.0f}%", (10, h - 10), (0, 0, 0), scale=0.65)

    return result

# ---------------------------------------------------------------
# Full per-frame pipeline
# ---------------------------------------------------------------
_debug_counter = 0
_cached_inf_ms = 0.0
_cached_fps    = 0.0
_cached_cpu_ms = 0.0
_cached_temp     = 0.0
_cached_cpu_used = 0.0
_cached_cpu_free = 100.0

def process_frame(bgr, outputs, mask_proc, bev, fitter, inf_ms, fps=None):
    global _debug_counter
    h, w = bgr.shape[:2]

    # 1. Hailo outputs -> binary mask
    t1 = time.perf_counter()
    binary_mask = yolo26_to_mask(outputs, h, w, SCORE_THRESHOLD, TOP_K)
    t2 = time.perf_counter()

    # 2. Morphology
    clean_mask = mask_proc.process(binary_mask)
    t3 = time.perf_counter()

    # 3. BEV
    bev_mask = bev.warp(clean_mask)
    t4 = time.perf_counter()

    # 4. Sliding windows
    fit = fitter.fit(bev_mask)
    t5 = time.perf_counter()

    # Per-step timings in ms
    ms_postproc  = (t2 - t1) * 1000
    ms_morph     = (t3 - t2) * 1000
    ms_bev       = (t4 - t3) * 1000
    ms_sliding   = (t5 - t4) * 1000
    ms_cpu_total = (t5 - t1) * 1000

    # System CPU% since last frame (via /proc/stat, all cores)
    global _cpu_stat_prev
    user_now, sys_now, idle_now, total_now = _read_cpu_stat()
    user_prev, sys_prev, idle_prev, total_prev = _cpu_stat_prev
    d_total  = total_now - total_prev
    d_user   = user_now  - user_prev
    d_sys    = sys_now   - sys_prev
    d_idle   = idle_now  - idle_prev
    cpu_pct_user   = d_user  / d_total * 100 if d_total > 0 else 0.0
    cpu_pct_sys    = d_sys   / d_total * 100 if d_total > 0 else 0.0
    cpu_pct_idle   = d_idle  / d_total * 100 if d_total > 0 else 0.0
    cpu_pct_single = cpu_pct_user + cpu_pct_sys
    _cpu_stat_prev = (user_now, sys_now, idle_now, total_now)

    # Update INF/TEMP cache every 90 frames
    global _cached_inf_ms, _cached_fps, _cached_cpu_ms, _cached_temp, _cached_cpu_used, _cached_cpu_free
    _debug_counter += 1
    if _debug_counter % 90 == 1:
        _cached_inf_ms   = inf_ms
        _cached_fps      = fps if fps else 0.0
        _cached_cpu_ms   = ms_cpu_total
        _cached_temp     = _read_temp()
        _cached_cpu_used = cpu_pct_user + cpu_pct_sys
        _cached_cpu_free = cpu_pct_idle
        cov_raw   = binary_mask.sum() / 255 / binary_mask.size * 100
        cov_clean = clean_mask.sum() / 255 / clean_mask.size * 100
        cov_bev   = bev_mask.sum() / 255 / bev_mask.size * 100
        print(f"[DBG] mask={cov_raw:.1f}%  clean={cov_clean:.1f}%  bev={cov_bev:.1f}%  "
              f"L={fit.left_found} R={fit.right_found}  CTE={fit.cte_meters}")
        print(f"[INF] hailo={inf_ms:.1f}ms  FPS={fps:.1f}" if fps else f"[INF] hailo={inf_ms:.1f}ms")
        print(f"[CPU] postproc={ms_postproc:.1f}ms  morph={ms_morph:.1f}ms  "
              f"bev={ms_bev:.1f}ms  sliding={ms_sliding:.1f}ms  "
              f"total_cpu={ms_cpu_total:.1f}ms")
        print(f"[SYS] user={cpu_pct_user:.1f}%  sys={cpu_pct_sys:.1f}%  "
              f"idle={cpu_pct_idle:.1f}%  used={cpu_pct_single:.1f}%  temp={_cached_temp:.0f}C")
        # Save masks for visual inspection
        cv2.imwrite("/home/debug_mask_raw.png",   binary_mask)
        cv2.imwrite("/home/debug_mask_clean.png", clean_mask)
        cv2.imwrite("/home/debug_mask_bev.png",   bev_mask)

    # 5. Visualization — geometry at original resolution, text on display
    result = draw_lane_overlay(bgr, fit, bev)
    return result, fit, _cached_inf_ms, _cached_fps, _cached_cpu_ms, _cached_temp, _cached_cpu_used, _cached_cpu_free

# ---------------------------------------------------------------
# Image mode
# ---------------------------------------------------------------
def run_image(hef, image_path):
    frame_bgr = cv2.imread(image_path)
    if frame_bgr is None:
        print(f"ERROR: could not read: {image_path}")
        sys.exit(1)

    h, w = frame_bgr.shape[:2]
    input_np = preprocess(frame_bgr, NET_SIZE)
    print(f"Image: {frame_bgr.shape}")

    with VDevice() as target:
        cfg = ConfigureParams.create_from_hef(hef, interface=HailoStreamInterface.PCIe)
        ng  = target.configure(hef, cfg)[0]
        with ng.activate(ng.create_params()):
            in_p  = InputVStreamParams.make(ng)
            out_p = OutputVStreamParams.make(ng, format_type=FormatType.FLOAT32)
            with InferVStreams(ng, in_p, out_p) as pipeline:
                input_name = list(in_p.keys())[0]
                data = {input_name: input_np}
                _ = pipeline.infer(data)  # warm-up
                t0 = time.perf_counter()
                outputs = pipeline.infer(data)
                inf_ms = (time.perf_counter() - t0) * 1000

    print(f"Inference: {inf_ms:.1f} ms")

    mask_proc = MaskPostProcessor()
    bev       = BEVTransform(w, h)
    fitter    = SlidingWindowsLaneFitter()

    result, fit, inf_ms_, _, cpu_ms, temp_, cpu_used_, cpu_free_ = \
        process_frame(frame_bgr, outputs, mask_proc, bev, fitter, inf_ms, fps=None)
    result = draw_text_overlay(result, fit, inf_ms_, cpu_ms=cpu_ms,
                               temp=temp_, model_name=MODEL_NAME,
                               cpu_used=cpu_used_, cpu_free=cpu_free_)

    base = os.path.splitext(os.path.basename(image_path))[0]
    out_path = f"result_{base}.jpg"
    cv2.imwrite(out_path, result)
    print(f"Result saved: {out_path}")

# ---------------------------------------------------------------
# Camera mode
# ---------------------------------------------------------------
def run_camera(hef):
    print(f"Starting camera ({CAM_WIDTH}x{CAM_HEIGHT} @ {CAM_FPS}fps)...")
    cam_cmd = [
        "rpicam-vid", "-t", "0", "--codec", "yuv420",
        "--width", str(CAM_WIDTH), "--height", str(CAM_HEIGHT),
        "--framerate", str(CAM_FPS),
        "--mode", "2304:1296:12:P",
        "--vflip", "--hflip",
        "-o", "-", "--nopreview",
    ]
    camera = subprocess.Popen(cam_cmd, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL)

    if REMOTE:
        display = None
        print("Mode --remote: MJPEG stream via stdout.")
    elif NO_DISPLAY:
        display = None
        print("Mode --no-display: no visual output, terminal only.")
    else:
        gst_env = dict(os.environ, XDG_RUNTIME_DIR="/run/user/200", WAYLAND_DISPLAY="wayland-1")
        gst_cmd = (
            f"gst-launch-1.0 fdsrc ! rawvideoparse format=bgr "
            f"width={DISPLAY_WIDTH} height={DISPLAY_HEIGHT} framerate={CAM_FPS}/1 ! "
            f"videoconvert ! queue ! waylandsink sync=false"
        )
        display = subprocess.Popen(gst_cmd, stdin=subprocess.PIPE, env=gst_env, shell=True)

    raw_frame_size = CAM_WIDTH * CAM_HEIGHT * 3 // 2

    mask_proc = MaskPostProcessor()
    bev       = BEVTransform(CAM_WIDTH, CAM_HEIGHT)
    fitter    = SlidingWindowsLaneFitter()

    try:
        with VDevice() as target:
            cfg = ConfigureParams.create_from_hef(hef, interface=HailoStreamInterface.PCIe)
            ng  = target.configure(hef, cfg)[0]
            with ng.activate(ng.create_params()):
                in_p  = InputVStreamParams.make(ng)
                out_p = OutputVStreamParams.make(ng, format_type=FormatType.FLOAT32)
                with InferVStreams(ng, in_p, out_p) as pipeline:
                    input_name = list(in_p.keys())[0]
                    print("Ready! Press Ctrl+C to stop.")
                    frame_count = 0
                    t_start = time.time()

                    while True:
                        raw = camera.stdout.read(raw_frame_size)
                        if len(raw) < raw_frame_size:
                            break

                        yuv = np.frombuffer(raw, dtype=np.uint8).reshape((CAM_HEIGHT * 3 // 2, CAM_WIDTH))
                        bgr = cv2.cvtColor(yuv, cv2.COLOR_YUV2BGR_I420)

                        input_np = preprocess(bgr, NET_SIZE)
                        t0 = time.perf_counter()
                        outputs = pipeline.infer({input_name: input_np})
                        inf_ms = (time.perf_counter() - t0) * 1000

                        frame_count += 1
                        fps = frame_count / (time.time() - t_start)

                        result, fit, inf_ms_, fps_, cpu_ms, temp_, cpu_used_, cpu_free_ = \
                            process_frame(bgr, outputs, mask_proc, bev, fitter, inf_ms, fps)

                        if REMOTE:
                            display_frame = cv2.resize(result, (DISPLAY_WIDTH, DISPLAY_HEIGHT))
                            display_frame = draw_text_overlay(display_frame, fit, inf_ms_, fps_,
                                                              cpu_ms, temp=temp_, model_name=MODEL_NAME,
                                                              cpu_used=cpu_used_, cpu_free=cpu_free_)
                            _, buf = cv2.imencode('.jpg', display_frame, [cv2.IMWRITE_JPEG_QUALITY, 80])
                            sys.stdout.buffer.write(buf.tobytes())
                            sys.stdout.buffer.flush()
                        elif display is not None:
                            display_frame = cv2.resize(result, (DISPLAY_WIDTH, DISPLAY_HEIGHT))
                            display_frame = draw_text_overlay(display_frame, fit, inf_ms_, fps_,
                                                              cpu_ms, temp=temp_, model_name=MODEL_NAME,
                                                              cpu_used=cpu_used_, cpu_free=cpu_free_)
                            display.stdin.write(display_frame.tobytes())
                            display.stdin.flush()

    except KeyboardInterrupt:
        print("\nStopped by user.")
    finally:
        camera.terminate()
        if display is not None:
            display.terminate()

# ---------------------------------------------------------------
# Main
# ---------------------------------------------------------------
def main():
    if not os.path.exists(HEF_PATH):
        print(f"ERROR: HEF not found: {HEF_PATH}")
        sys.exit(1)

    print(f"Modo:      {MODE}")
    print(f"HEF:       {HEF_PATH}")
    print(f"Threshold: {SCORE_THRESHOLD}")

    hef = HEF(HEF_PATH)

    # Auto-detect NET_SIZE and PROTO_SIZE from HEF
    global NET_SIZE, PROTO_SIZE
    input_info = hef.get_input_vstream_infos()[0]
    NET_SIZE = input_info.shape[1]  # assumes square input (H=W)
    PROTO_SIZE = NET_SIZE // 4
    print(f"HEF loaded: NET_SIZE={NET_SIZE} PROTO_SIZE={PROTO_SIZE}")

    if MODE == "image":
        if not IMAGE_PATH:
            print("ERROR: specify the image path")
            sys.exit(1)
        if not os.path.exists(IMAGE_PATH):
            print(f"ERROR: image not found: {IMAGE_PATH}")
            sys.exit(1)
        run_image(hef, IMAGE_PATH)
    else:
        run_camera(hef)


if __name__ == "__main__":
    main()
