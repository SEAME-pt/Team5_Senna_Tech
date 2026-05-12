"""
LKA Lane Detector
=================
Loads a YOLOv8-seg model (best.pt for development, or .hef for Hailo production)
and runs inference on a single RGB frame, returning a binary lane mask.

The mask is then passed to the classical pipeline:
    BEV Warp → Sliding Windows → Polyfit → CTE
"""

import cv2
import numpy as np
from ultralytics import YOLO


class LaneDetector:
    """
    Wraps YOLOv8-seg inference.
    Accepts a RGB frame and returns a binary mask (uint8, 0 or 255).
    """

    def __init__(self,
                 model_path: str,
                 conf_threshold: float = 0.25,
                 input_size: int = 640):
        """
        Args:
            model_path:      Path to best.pt or .onnx file.
            conf_threshold:  Minimum confidence to accept a mask prediction.
            input_size:      Image size used during training (640).
        """
        self.model = YOLO(model_path)
        self.conf_threshold = conf_threshold
        self.input_size = input_size

        print(f"[LaneDetector] Model loaded from: {model_path}")

    def predict(self, frame_rgb: np.ndarray) -> np.ndarray:
        """
        Run inference on a single RGB frame.

        Args:
            frame_rgb: H x W x 3 numpy array in RGB format.

        Returns:
            binary_mask: H x W uint8 array.
                         255 = lane marking pixel
                         0   = background
        """
        h, w = frame_rgb.shape[:2]

        # Run YOLOv8-seg inference
        results = self.model.predict(
            source=frame_rgb,
            imgsz=self.input_size,
            conf=self.conf_threshold,
            verbose=False
        )

        # Build empty mask (same size as input frame)
        binary_mask = np.zeros((h, w), dtype=np.uint8)

        result = results[0]

        # No detections -> return empty mask
        if result.masks is None:
            return binary_mask

        # Merge all detected lane masks into one binary mask
        for i, mask_tensor in enumerate(result.masks.data):
            # mask_tensor is a float32 tensor on GPU/CPU, shape (H', W')
            mask_np = mask_tensor.cpu().numpy()

            # Resize mask to original frame size
            mask_resized = cv2.resize(
                mask_np,
                (w, h),
                interpolation=cv2.INTER_LINEAR
            )

            # Threshold to binary
            _, mask_binary = cv2.threshold(mask_resized, 0.5, 255, cv2.THRESH_BINARY)
            binary_mask = cv2.bitwise_or(binary_mask, mask_binary.astype(np.uint8))

        return binary_mask

    def predict_with_debug(self, frame_rgb: np.ndarray):
        """
        Same as predict() but also returns a debug overlay image (BGR).
        Useful during development to visualise detections.

        Returns:
            binary_mask:  H x W uint8 array (255 = lane)
            debug_image:  H x W x 3 BGR image with green overlay
        """
        binary_mask = self.predict(frame_rgb)

        # Convert frame to BGR for OpenCV drawing
        debug_image = cv2.cvtColor(frame_rgb, cv2.COLOR_RGB2BGR)

        # Draw green overlay on detected lane pixels
        overlay = debug_image.copy()
        overlay[binary_mask == 255] = (0, 255, 0)
        debug_image = cv2.addWeighted(debug_image, 0.6, overlay, 0.4, 0)

        return binary_mask, debug_image
