from ultralytics import YOLO
import cv2
import numpy as np


class YOLOv8Detector:

    def __init__(self, model_path):
        self.model = YOLO(model_path)

    def infer(self, frame):

        results = self.model.predict(
            source=frame,
            imgsz=640,
            conf=0.3,
            device=0,
            verbose=False
        )

        result = results[0]
        output = frame.copy()

        lane_mask = np.zeros((frame.shape[0], frame.shape[1]), dtype=np.uint8)

        if result.masks is not None:

            masks = result.masks.data.cpu().numpy()

            for mask in masks:

                mask = cv2.resize(mask, (frame.shape[1], frame.shape[0]))
                mask = (mask > 0.5).astype(np.uint8)

                lane_mask = np.maximum(lane_mask, mask)

                overlay = np.zeros_like(frame)
                overlay[mask == 1] = (0,255,0)

                output = cv2.addWeighted(output, 1.0, overlay, 0.4, 0)

        return output, lane_mask