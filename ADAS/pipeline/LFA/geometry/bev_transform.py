import cv2
import numpy as np

class BEVTransform:
    #   !!!!!!!!!!  se for mudar os valores deixar esses comentados, foi o nosso melhor até o momento
    DEFAULT_SRC = np.float32([
        [0.10000000149011612, 0.5299999713897705], 
        [0.9200000166893005, 0.5299999713897705], 
        [1.309999942779541, 0.7599999904632568], 
        [-0.28999999165534973, 0.7599999904632568]
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