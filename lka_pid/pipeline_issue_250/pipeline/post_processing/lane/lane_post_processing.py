import cv2
import numpy as np
import logging


class YoloSegDecoder:
    def __init__(self, score_threshold=0.25, top_k=200, debug=False):
        self.score_threshold = score_threshold
        self.top_k = top_k
        self.debug = debug
        self._output_keys = {}
        self._output_mode = None
        self.num_channels = None

    def _find_output_keys(self, outputs):
        if self._output_keys:
            return self._output_keys

        proto_candidate = None
        for name, val in outputs.items():
            s = val.shape
            if len(s) == 4 and 32 in s:
                spatial_dims = [d for d in s if d != 1 and d != 32]
                if len(spatial_dims) >= 2 and spatial_dims[0] == spatial_dims[1]:
                    proto_candidate = name
                    break
                elif len(spatial_dims) == 1 and spatial_dims[0] < 1000:
                    proto_candidate = name

        if proto_candidate:
            self._output_keys["proto"] = proto_candidate

        non_proto = {n: v for n, v in outputs.items() if n != proto_candidate}

        pre_concat4_bbox, pre_concat4_score, pre_concat4_mask = None, None, None

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
            self._output_mode = "pre_concat4"
            self._output_keys["bbox"] = pre_concat4_bbox
            self._output_keys["score"] = pre_concat4_score
            self._output_keys["mask"] = pre_concat4_mask
            self.num_channels = 4 + 1 + 32
            return self._output_keys

        bbox_scales, score_scales, mask_scales = {}, {}, {}

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
            self._output_mode = "per_scale"
            self._output_keys["bbox_scales"] = bbox_scales
            self._output_keys["score_scales"] = score_scales
            self._output_keys["mask_scales"] = mask_scales
            self.num_channels = 4 + 1 + 32
        else:
            self._output_mode = "concat4"
            for name, val in non_proto.items():
                s = val.shape
                if any(d >= 37 and d <= 40 for d in s):
                    self._output_keys["det"] = name
                    self.num_channels = [d for d in s if 37 <= d <= 40][0]
                    break

        return self._output_keys

    def decode_to_mask(self, outputs, orig_h, orig_w):
        keys = self._find_output_keys(outputs)
        if "proto" not in keys:
            return np.zeros((orig_h, orig_w), dtype=np.uint8)

        proto_raw = outputs[keys["proto"]]

        if self._output_mode == "pre_concat4":
            def squeeze_8400(name):
                t = outputs[name].astype(np.float32)
                return t.reshape(8400, -1)

            score_t = squeeze_8400(keys["score"])
            mask_t = squeeze_8400(keys["mask"])
            scores = score_t.squeeze(1)
            mask_coeffs = mask_t

        elif self._output_mode == "per_scale":
            def concat_scales(scale_dict):
                tensors = []
                for h in sorted(scale_dict.keys(), reverse=True):
                    t = outputs[scale_dict[h]].astype(np.float32)
                    t = np.transpose(t, (0, 3, 1, 2))
                    tensors.append(t.reshape(1, t.shape[1], -1))
                return np.concatenate(tensors, axis=2)

            score = concat_scales(keys["score_scales"])
            mask_coef = concat_scales(keys["mask_scales"])
            scores = score.squeeze()
            mask_coeffs = mask_coef.squeeze(0).T

        else:
            if "det" not in keys:
                return np.zeros((orig_h, orig_w), dtype=np.uint8)
            det_raw = outputs[keys["det"]]
            det = det_raw.squeeze().astype(np.float32)
            if self.num_channels and det.shape[0] == self.num_channels:
                det = det.T
            nc = det.shape[1] - 4 - 32
            scores = det[:, 4:4 + nc].max(axis=1)
            mask_coeffs = det[:, 4 + nc:]

        if scores.max() - scores.min() < 0.01:
            scores = np.linalg.norm(mask_coeffs, axis=1).astype(np.float32)
            scores = (scores - scores.min()) / (scores.max() - scores.min() + 1e-6)

        proto = proto_raw.squeeze(0).astype(np.float32)
        if proto.shape[-1] == 32:
            proto = np.transpose(proto, (2, 0, 1))

        n_candidates = min(self.top_k, len(scores))
        top_idx = np.argpartition(scores, -n_candidates)[-n_candidates:]
        top_scores = scores[top_idx]
        top_coeffs = mask_coeffs[top_idx]

        valid = top_scores > self.score_threshold
        if not np.any(valid):
            return np.zeros((orig_h, orig_w), dtype=np.uint8)

        valid_scores = top_scores[valid]
        valid_coeffs = top_coeffs[valid]

        P = proto.shape[1]
        proto_flat = proto.reshape(32, -1)

        raw_masks = valid_coeffs @ proto_flat
        raw_masks = 1.0 / (1.0 + np.exp(-np.clip(raw_masks, -20, 20)))
        raw_masks = raw_masks.reshape(len(valid_scores), P, P)

        weights = valid_scores / np.maximum(valid_scores.sum(), 1e-6)
        combined = (weights[:, None, None] * raw_masks).sum(axis=0)

        mask_resized = cv2.resize(combined, (orig_w, orig_h))
        thr = max(float(mask_resized.mean() + 0.1 * mask_resized.std()), 0.3)
        
        if self.debug:
            logging.debug(f"[YoloSegDecoder] Mask mean: {mask_resized.mean():.4f}, threshold: {thr:.4f}")

        _, binary = cv2.threshold(mask_resized, thr, 255, cv2.THRESH_BINARY)
        return binary.astype(np.uint8)


class MaskFilters:
    def __init__(self, close_kernel=(5, 15), open_kernel=(5, 5), debug=False):
        self.close_k = cv2.getStructuringElement(cv2.MORPH_RECT, close_kernel)
        self.open_k = cv2.getStructuringElement(cv2.MORPH_RECT, open_kernel)
        self.debug = debug

    def process(self, mask):
        closed = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, self.close_k)
        opened = cv2.morphologyEx(closed, cv2.MORPH_OPEN, self.open_k)
        
        if self.debug:
            non_zero = np.count_nonzero(opened)
            logging.debug(f"[MaskFilters] Post-filter non-zero pixels: {non_zero}")
            
        return opened
