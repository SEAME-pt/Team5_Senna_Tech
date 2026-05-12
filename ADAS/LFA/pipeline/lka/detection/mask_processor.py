"""
Mask Post-Processor
===================
Applies morphological operations to the raw binary mask produced by YOLOv8-seg.

Why is this needed?
- The model may produce dashed / fragmented lane markings (especially from CARLA data).
- Sliding Windows works best with continuous lane regions.
- MORPH_CLOSE fills small gaps; MORPH_OPEN removes isolated noise.
"""

import cv2
import numpy as np


class MaskPostProcessor:
    """
    Cleans up the binary lane mask before passing it to the BEV / Sliding Windows.
    """

    def __init__(self,
                 close_kernel_size: tuple = (5, 15),
                 open_kernel_size: tuple = (5, 5)):
        """
        Args:
            close_kernel_size: (width, height) of the vertical closing kernel.
                               Taller kernel closes gaps along the lane direction.
            open_kernel_size:  (width, height) of the opening kernel.
                               Removes small isolated noise blobs.
        """
        # Vertical kernel -> closes gaps between dashed line segments
        self.close_kernel = cv2.getStructuringElement(
            cv2.MORPH_RECT, close_kernel_size
        )
        # Square kernel -> removes small noise
        self.open_kernel = cv2.getStructuringElement(
            cv2.MORPH_RECT, open_kernel_size
        )

    def process(self, binary_mask: np.ndarray) -> np.ndarray:
        """
        Apply closing then opening to the binary mask.

        Args:
            binary_mask: H x W uint8 array (255 = lane, 0 = background).

        Returns:
            cleaned_mask: H x W uint8 array with gaps filled and noise removed.
        """
        # Step 1: CLOSE - dilate then erode → fills gaps between dashes
        closed = cv2.morphologyEx(binary_mask, cv2.MORPH_CLOSE, self.close_kernel)

        # Step 2: OPEN - erode then dilate → removes small isolated blobs
        cleaned = cv2.morphologyEx(closed, cv2.MORPH_OPEN, self.open_kernel)

        return cleaned
