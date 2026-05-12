"""
Bird's Eye View (BEV) Transform
================================
Applies a perspective warp to convert the front-facing camera frame into a
top-down (bird's eye) view.

Why BEV?
- In BEV, parallel lanes remain parallel → polyfit gives accurate curvature.
- Pixel distances in BEV can be mapped to real-world meters.
- Sliding Windows works much more reliably on BEV than on perspective images.

Calibration:
- src_points: four points on the road in the original (perspective) image.
              These should form a trapezoid that maps to a rectangle in BEV.
- dst_points: the corresponding rectangle in the BEV image.
- These values MUST be tuned to your specific camera and mounting position.
"""

import cv2
import numpy as np

class BEVTransform:
    """
    Performs perspective transformation (Bird's Eye View) for lane detection.
    """
    DEFAULT_SRC = np.float32([[0.18000000715255737, 0.4300000071525574], [0.8999999761581421, 0.4300000071525574], [1.5099999904632568, 1.0], [-0.4300000071525574, 1.0]])
    DEFAULT_DST = np.float32([
        [0.25, 0.00],   # top-left
        [0.75, 0.00],   # top-right
        [0.75, 1.00],   # bottom-right
        [0.25, 1.00]    # bottom-left
    ])

    def __init__(self,
                 image_width: int,
                 image_height: int,
                 src_points: np.ndarray = None,
                 dst_points: np.ndarray = None):
        
        self.w = image_width
        self.h = image_height

        self.src = src_points if src_points is not None else self.DEFAULT_SRC
        self.dst = dst_points if dst_points is not None else self.DEFAULT_DST

        src_px = self._to_pixels(self.src)
        dst_px = self._to_pixels(self.dst)

        # Transformation matrices
        self.M     = cv2.getPerspectiveTransform(src_px, dst_px)
        self.M_inv = cv2.getPerspectiveTransform(dst_px, src_px)

        print(f"[BEVTransform] Calibrado: {image_width}x{image_height}")

    def _to_pixels(self, points_frac: np.ndarray) -> np.ndarray:
        px = points_frac.copy()
        px[:, 0] *= self.w
        px[:, 1] *= self.h
        return px

    def warp(self, image: np.ndarray) -> np.ndarray:
        return cv2.warpPerspective(image, self.M, (self.w, self.h))

    def unwarp(self, bev_image: np.ndarray) -> np.ndarray:
        return cv2.warpPerspective(bev_image, self.M_inv, (self.w, self.h))

    def visualise_calibration(self, frame_bgr: np.ndarray) -> np.ndarray:
        src_draw = self._to_pixels(self.src).astype(np.int32)
        dst_draw = self._to_pixels(self.dst).astype(np.int32)

        # Original with trapezoid
        orig_vis = frame_bgr.copy()
        cv2.polylines(orig_vis, [src_draw], isClosed=True, color=(0, 255, 0), thickness=3)

        # BEV with rectangle
        bev_frame = self.warp(frame_bgr)
        cv2.polylines(bev_frame, [dst_draw], isClosed=True, color=(0, 255, 255), thickness=3)

        return np.concatenate([orig_vis, bev_frame], axis=1)