import threading
import time

from .aruco_detector import ArucoDetector
from  map.track_map import GridPos


class ArucoWorker(threading.Thread):

    ARUCO_GRID_MAP = {
        0: GridPos(row=17, col=14),
        1: GridPos(row=12, col=14),
        2: GridPos(row=7, col=14),
        3: GridPos(row=2, col=14),
        4: GridPos(row=0, col=11),
        5: GridPos(row=0, col=7),
        6: GridPos(row=0, col=3),
        7: GridPos(row=4, col=0),
        8: GridPos(row=9, col=5),
        9: GridPos(row=14, col=3),
        11: GridPos(row=18, col=6),
        12: GridPos(row=18, col=9),
        13: GridPos(row=15, col=8),
        14: GridPos(row=18, col=12),
    }


    def __init__(self, frequency_hz=5):
        super().__init__(daemon=True)

        self.detector = ArucoDetector()

        self.frequency_hz = frequency_hz
        self.period = 1.0 / frequency_hz

        self.frame = None

        self.last_detection = []
        self.timestamp = None

        self.lock = threading.Lock()

        self.running = True

    def update_frame(self, frame):
        with self.lock:
            self.frame = frame.copy()

    def get_detections(self):

        """
        Detect ArUco markers in the input frame and estimate the closest one.

        Returns:
            dict:
                {
                    "id": int,          # ID of the closest detected marker
                    "distance": float   # Estimated distance in meters
                }

            If no markers are detected.
                {
                    "id": None,
                    "distance": None
                }
        """
        
        with self.lock:
            if self.last_detection is None:
                return {
                    "id": None,
                    "distance": None
                }

            return self.last_detection.copy()

    def stop(self):
        self.running = False

    def run(self):
        while self.running:
            frame = None

            with self.lock:
                if self.frame is not None:
                    frame = self.frame

            if frame is not None:
                detections = self.detector.detect(frame)

                with self.lock:
                    self.last_detection = detections
                    self.timestamp = time.time()

            time.sleep(self.period)

    def current_grid(self, detection, current_grid_position):
        if detection is None:
            return current_grid_position

        marker_id = detection.get("id")
        distance = detection.get("distance")

        if marker_id is None or distance is None:
            return current_grid_position

        # Só considera válido se estiver suficientemente perto
        if distance > 0.40:
            return current_grid_position

        return self.ARUCO_GRID_MAP.get(marker_id)