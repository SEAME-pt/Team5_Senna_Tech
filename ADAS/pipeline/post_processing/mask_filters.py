"""
Cleans and improves the binary mask of the tracks using morphological operations.
Operations applied sequentially:
1. CLOSE: fills small gaps and holes in the tracks
2. OPEN: removes noise and small isolated artifacts
Rectangular kernels are wider horizontally for vertical tracks.
"""

import cv2

class MaskFilters:
    def __init__(self, close_kernel=(5, 15), open_kernel=(5, 5)):
        self.close_k = cv2.getStructuringElement(cv2.MORPH_RECT, close_kernel)
        self.open_k  = cv2.getStructuringElement(cv2.MORPH_RECT, open_kernel)

    def process(self, mask):
        closed = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, self.close_k)
        return cv2.morphologyEx(closed, cv2.MORPH_OPEN, self.open_k)