import threading
import subprocess
import numpy as np
import cv2

class CameraReader:
    def __init__(self, cam_cmd, width, height):
        self.width = width
        self.height = height

        self.frame_size = width * height * 3 // 2

        self.latest_frame = None
        self.running = True
        self.lock = threading.Lock()

        self.camera = subprocess.Popen(
            cam_cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.DEVNULL
        )

        self.thread = threading.Thread(target=self.update, daemon=True)
        self.thread.start()

    def read_exact(self, pipe, size):
        buf = b''
        while len(buf) < size:
            chunk = pipe.read(size - len(buf))
            if not chunk:
                return None
            buf += chunk
        return buf

    def update(self):
        while self.running:
            raw = self.read_exact(self.camera.stdout, self.frame_size)
            if raw is None:
                continue

            yuv = np.frombuffer(raw, dtype=np.uint8).reshape(
                (self.height * 3 // 2, self.width)
            )

            frame = cv2.cvtColor(yuv, cv2.COLOR_YUV2BGR_I420)

            with self.lock:
                self.latest_frame = frame

    def get_frame(self):
        with self.lock:
            if self.latest_frame is None:
                return None
            return self.latest_frame.copy()

    def stop(self):
        self.running = False
        self.camera.terminate()