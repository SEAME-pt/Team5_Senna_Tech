import cv2
import numpy as np
import subprocess
import threading
import logging


class Camera:
    def __init__(self, width, height, fps, debug=False):
        self.width = width
        self.height = height
        self.fps = fps
        self.frame_size = width * height * 3 // 2
        self.debug = debug

        self.process = None
        self._latest_frame = None
        self._running = False
        self._lock = threading.Lock()
        self._thread = None

    def _check_existing(self):
        result = subprocess.run(["pgrep", "-f", "rpicam-vid"], capture_output=True, text=True)
        if result.stdout.strip():
            for pid in result.stdout.strip().split("\n"):
                logging.warning("[CAMERA] rpicam-vid already running with PID=%s. If safe, run: kill %s", pid, pid)
            return True
        return False

    def _read_exact(self, pipe, size):
        buf = b''
        while len(buf) < size:
            chunk = pipe.read(size - len(buf))
            if not chunk:
                return None
            buf += chunk
        return buf

    def _capture_loop(self):
        while self._running:
            raw = self._read_exact(self.process.stdout, self.frame_size)
            if raw is None:
                continue
            yuv = np.frombuffer(raw, dtype=np.uint8).reshape((self.height * 3 // 2, self.width))
            frame = cv2.cvtColor(yuv, cv2.COLOR_YUV2RGB_I420)
            if self.debug:
                logging.debug("[CAMERA] frame shape=%s dtype=%s", frame.shape, frame.dtype)
            with self._lock:
                self._latest_frame = frame

    def __enter__(self):
        if self._check_existing():
            return self
        cam_cmd = [
            "rpicam-vid", "-t", "0", "--codec", "yuv420",
            "--width", str(self.width), "--height", str(self.height),
            "--framerate", str(self.fps), "--mode", "640:360:8:P",
            "--exposure", "sport", "--denoise", "off",
            "--shutter", "3500", "--vflip", "--hflip", "-o", "-", "--nopreview"
        ]
        self.process = subprocess.Popen(cam_cmd, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL)
        self._running = True
        self._thread = threading.Thread(target=self._capture_loop, daemon=True)
        self._thread.start()
        logging.info("[CAMERA] Started %dx%d @ %dfps", self.width, self.height, self.fps)
        return self

    def get_frame(self):
        with self._lock:
            if self._latest_frame is None:
                return None
            return self._latest_frame.copy()

    def stop(self):
        self._running = False
        if self.process is not None:
            self.process.terminate()
            self.process.wait()
            logging.info("[CAMERA] Stopped")

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.stop()
