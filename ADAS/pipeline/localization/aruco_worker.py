import threading
import time

from .aruco_detector import ArucoDetector


class ArucoWorker(threading.Thread):
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
        with self.lock:
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