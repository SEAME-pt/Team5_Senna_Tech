import cv2


class ArucoDetector:
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
        corners, ids, rejected = self.detector.detectMarkers(frame)

        detections = []

        if ids is None:
            return detections

        for marker_corners, marker_id in zip(corners, ids.flatten()):
            detections.append(
                {
                    "id": int(marker_id),
                    "corners": marker_corners[0],
                }
            )

        return detections