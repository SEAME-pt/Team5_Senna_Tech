import cv2
import numpy as np

def draw_lane_overlay(frame_rgb, fit_result, bev):
    h, w = frame_rgb.shape[:2]
    result = frame_rgb.copy()
    y_vals = np.arange(0, h)

    def poly_pts(f):
        if f is None: return None
        x = f[0]*y_vals**2 + f[1]*y_vals + f[2]
        return np.stack([x, y_vals], axis=1).astype(np.int32)

    if fit_result.left_fit is None and fit_result.right_fit is None:
        return result

    overlay = np.zeros_like(frame_rgb)
    lp = poly_pts(fit_result.left_fit)
    rp = poly_pts(fit_result.right_fit)

    if lp is not None and rp is not None:
        pts = np.vstack([lp, rp[::-1]])
        cv2.fillPoly(overlay, [pts], (0, 150, 0))
        cx = (lp[:, 0] + rp[:, 0]) / 2
        cp = np.stack([cx, y_vals], axis=1).astype(np.int32)
        cv2.polylines(overlay, [cp], False, (0, 255, 255), 2)

    if lp is not None:
        l_color = (0, 255, 255) if getattr(fit_result, 'left_is_virtual', False) else (0, 0, 255)
        cv2.polylines(overlay, [lp], False, l_color, 10)

    if rp is not None:
        r_color = (0, 255, 255) if getattr(fit_result, 'right_is_virtual', False) else (255, 0, 0)
        cv2.polylines(overlay, [rp], False, r_color, 10)

    unwarped = bev.unwarp(overlay)
    result = cv2.addWeighted(result, 1.0, unwarped, 0.4, 0)

    try:
        src_pts = (bev.DEFAULT_SRC * [w, h]).astype(np.int32)
        cv2.polylines(result, [src_pts], True, (255, 0, 255), 2)
    except:
        pass

    return result


def draw_text_overlay(frame, fit_result, fps=None, inf_ms=None):
    h, w = frame.shape[:2]
    result = frame

    def put(txt, pos, color, scale=1.2, thick=2):
        cv2.putText(result, txt, pos, cv2.FONT_HERSHEY_SIMPLEX, scale, color, thick)

    label = ""
    if inf_ms is not None: label += f"Hailo: {inf_ms:.1f}ms  "
    if fps is not None: label += f"FPS: {fps:.1f}"
    put(label, (10, h - 35), (255, 255, 255), scale=0.6)

    return result
