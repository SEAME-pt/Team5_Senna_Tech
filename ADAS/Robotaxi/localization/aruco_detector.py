import cv2
import numpy as np


class ArucoDetector:
    TAG_SIZE_M = 0.04
    FOCAL_LENGTH = 370

    def __init__(self):
        self.dictionary = cv2.aruco.getPredefinedDictionary(
            cv2.aruco.DICT_4X4_50
        )

        self.parameters = cv2.aruco.DetectorParameters()

        self.detector = cv2.aruco.ArucoDetector(
            self.dictionary,
            self.parameters,
        )

    def detect(self, frame):
        corners, ids, _ = self.detector.detectMarkers(frame)

        if ids is None:
            return {
                "id": None,
                "distance_m": None,
                "distance_cm": None,
            }

        closest = None

        for marker_corners, marker_id in zip(corners, ids.flatten()):
            pts = marker_corners[0]

            pixel_width = np.linalg.norm(pts[1] - pts[0])

            if pixel_width <= 0:
                continue

            distance_m = (
                self.TAG_SIZE_M * self.FOCAL_LENGTH
            ) / pixel_width

            if closest is None or distance_m < closest["distance_m"]:
                closest = {
                    "id": int(marker_id),
                    "distance_m": distance_m,
                    "distance_cm": distance_m * 100.0,
                }

        if closest is None:
            return {
                "id": None,
                "distance_m": None,
                "distance_cm": None,
            }

        return closest