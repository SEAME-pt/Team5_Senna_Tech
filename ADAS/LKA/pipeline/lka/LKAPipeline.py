"""
LKA Pipeline
============
Orchestrates the full Lane Keeping Assist pipeline:

    RGB frame
        │
        ▼
    LaneDetector          (YOLOv8-seg → binary mask)
        │
        ▼
    MaskPostProcessor     (morphology → fill dashed gaps)
        │
        ▼
    BEVTransform.warp()   (perspective → top-down)
        │
        ▼
    SlidingWindowsLaneFitter.fit()   (detect pixels → polyfit)
        │
        ├── LaneFitResult.cte_meters  → PID controller
        └── LaneFitResult.*_fit       → LaneVisualiser
"""

import cv2
import numpy as np
from typing import Tuple, Optional

from .detection.lane_detector    import LaneDetector
from .detection.mask_processor   import MaskPostProcessor
from .geometry.bev_transform     import BEVTransform
from .geometry.sliding_windows   import SlidingWindowsLaneFitter, LaneFitResult
from .visualisation.lane_visualiser import LaneVisualiser


class LKAPipeline:
    """
    Full LKA perception pipeline.
    Instantiate once, then call process() on every frame.
    """

    def __init__(self,
                 model_path: str,
                 image_width: int,
                 image_height: int,
                 conf_threshold: float = 0.25,
                 bev_src_points: np.ndarray = None,
                 bev_dst_points: np.ndarray = None,
                 n_windows: int = 9,
                 window_margin: int = 80,
                 lane_width_meters: float = 3.7):
        """
        Args:
            model_path:         Path to YOLOv8-seg weights (.pt or .onnx).
            image_width:        Camera frame width in pixels.
            image_height:       Camera frame height in pixels.
            conf_threshold:     YOLOv8 confidence threshold (0.0–1.0).
            bev_src_points:     4x2 float32 array of BEV source points (fractions).
                                If None, BEVTransform defaults are used.
            bev_dst_points:     4x2 float32 array of BEV destination points (fractions).
            n_windows:          Number of sliding windows.
            window_margin:      Half-width of each sliding window (pixels).
            lane_width_meters:  Real-world lane width in metres.
        """
        print("[LKAPipeline] Initialising...")

        # --- Smoothing Variables ---
        self.smoothed_cte = 0.0
        self.alpha = 0.7

        # --- Detection (YOLOv8-seg) ---
        self.detector = LaneDetector(
            model_path=model_path,
            conf_threshold=conf_threshold
        )

        # --- Mask post-processing ---
        self.mask_processor = MaskPostProcessor(
            close_kernel_size=(5, 5),
            open_kernel_size=(5, 5)
        )

        # --- BEV transform ---
        self.bev = BEVTransform(
            image_width=image_width,
            image_height=image_height,
            src_points=bev_src_points,
            dst_points=bev_dst_points
        )

        # --- Sliding windows + polyfit ---
        self.fitter = SlidingWindowsLaneFitter(
            n_windows=n_windows,
            margin=window_margin,
            lane_width_meters=lane_width_meters
        )

        # --- Visualiser ---
        self.visualiser = LaneVisualiser(bev=self.bev)

        print("[LKAPipeline] Ready.")

    def process(self,
                frame_rgb: np.ndarray,
                draw_debug: bool = False) -> Tuple[LaneFitResult, np.ndarray]:
        """
        Process one RGB frame through the full pipeline.

        Args:
            frame_rgb:  H x W x 3 numpy array in RGB format.
            draw_debug: If True, saves intermediate steps into LaneFitResult.debug_image.

        Returns:
            fit_result:  LaneFitResult with polynomial coefficients and CTE.
            annotated:   BGR frame with lane overlay drawn.
        """
        # Convert to BGR for OpenCV operations later
        frame_bgr = cv2.cvtColor(frame_rgb, cv2.COLOR_RGB2BGR)

        # ── Step 1: YOLOv8-seg inference ─────────────────────────────────────
        binary_mask = self.detector.predict(frame_rgb)

        cv2.imshow("binary mask", binary_mask)

        # ── Step 2: Morphological cleanup ────────────────────────────────────
        clean_mask = self.mask_processor.process(binary_mask)

        # ── Step 3: Bird's Eye View warp ─────────────────────────────────────
        bev_mask = self.bev.warp(clean_mask)

        # ── Step 4: Sliding Windows + Polyfit ────────────────────────────────
        fit_result = self.fitter.fit(bev_mask, draw_debug=draw_debug)

        # --- Smoothing of CTE ---
        if fit_result.cte_normalized is not None:

            self.smoothed_cte = (
                self.alpha * fit_result.cte_normalized +
                (1.0 - self.alpha) * self.smoothed_cte
            )

            fit_result.cte_normalized = self.smoothed_cte
        else:
            # and lose the track, we reset smoothly or keep the last one (here we reset).
            self.smoothed_cte = 0.0

        # ── Step 5: Visualize on original frame\ ───────────────────────────────
        annotated = self.visualiser.draw(frame_bgr, fit_result)

        return fit_result, annotated

    def calibrate_bev(self, frame_rgb: np.ndarray) -> np.ndarray:
        """
        Helper to visually inspect the BEV calibration.
        Returns a side-by-side image: original | BEV.
        Use this to tune bev_src_points / bev_dst_points.

        Args:
            frame_rgb: A straight-road frame from CARLA.

        Returns:
            calibration_image: BGR side-by-side visualisation.
        """
        frame_bgr = cv2.cvtColor(frame_rgb, cv2.COLOR_RGB2BGR)
        return self.bev.visualise_calibration(frame_bgr)
