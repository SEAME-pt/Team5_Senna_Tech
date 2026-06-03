import cv2
import numpy as np


class ArucoDetector:
    # This value MUST match the printed tag size for correct distance estimation.
    # Example: 4 cm tag -> 0.04 m
    TAG_SIZE_M = 0.04
    
    # FOCAL_LENGTH = (pixel_width * real_distance) / real_tag_size
    #
    # Higher value => object appears "closer" in estimation
    # Lower value  => object appears "farther" in estimation
    FOCAL_LENGTH = 370

    def __init__(self):
        self.dictionary = cv2.aruco.getPredefinedDictionary(
            cv2.aruco.DICT_4X4_50
        )

        self.parameters = cv2.aruco.DetectorParameters()

        self.detector = cv2.aruco.ArucoDetector(
            self.dictionary,
            self.parameters
        )

    def detect(self, frame):
        corners, ids, _ = self.detector.detectMarkers(frame)

        if ids is None:
            return None

        closest = None

        for marker_corners, marker_id in zip(corners, ids.flatten()):

            pts = marker_corners[0]

            pixel_width = np.linalg.norm(
                pts[1] - pts[0]
            )

            distance = (
                self.TAG_SIZE_M * self.FOCAL_LENGTH
            ) / pixel_width

            if closest is None or distance < closest["distance"]:
                closest = {
                    "id": int(marker_id),
                    "distance": round(distance, 2)
                }

        return closest