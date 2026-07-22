import threading
import time

from .aruco_detector import ArucoDetector
from map.track_map import get_grid_pos_from_aruco_id


class ArucoWorker(threading.Thread):
    def __init__(self, frequency_hz=5):
        super().__init__(daemon=True)

        self.detector = ArucoDetector()

        self.frequency_hz = frequency_hz
        self.period = 1.0 / frequency_hz

        self.frame = None

        self.last_detection = {
            "id": None,
            "distance_m": None,
            "distance_cm": None,
        }

        self.timestamp = None
        self.lock = threading.Lock()
        self.running = True

    def update_frame(self, frame):
        with self.lock:
            self.frame = frame.copy()

    def get_detection(self):
        with self.lock:
            return self.last_detection.copy()

    def get_detections(self):
        return self.get_detection()

    def stop(self):
        self.running = False

    def run(self):
        while self.running:
            frame = None

            with self.lock:
                if self.frame is not None:
                    frame = self.frame.copy()

            if frame is not None:
                detection = self.detector.detect(frame)

                with self.lock:
                    self.last_detection = detection
                    self.timestamp = time.time()

            time.sleep(self.period)

    def current_grid(self, current_grid_position, max_distance_m=0.50):
        detection = self.get_detection()

        marker_id = detection.get("id")
        distance_m = detection.get("distance_m")

        if marker_id is None or distance_m is None:
            return current_grid_position

        if distance_m > max_distance_m:
            return current_grid_position

        marker_grid_pos = get_grid_pos_from_aruco_id(marker_id)

        if marker_grid_pos is None:
            return current_grid_position

        return marker_grid_pos

    def is_close_to_marker(self, expected_id, max_distance_m=0.15):
        detection = self.get_detection()

        marker_id = detection.get("id")
        distance_m = detection.get("distance_m")

        if marker_id is None or distance_m is None:
            return False

        return marker_id == expected_id and distance_m <= max_distance_m