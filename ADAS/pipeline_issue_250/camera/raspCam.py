import cv2
import numpy as np
import subprocess
import logging

class Camera:
    def __init__(self, width, height, fps, debug=False):
        # Store camera resolution and frame rate
        self.width = width
        self.height = height
        self.fps = fps
        # YUV420 frame size in bytes (1.5 bytes per pixel)
        self.frame_size = width * height * 3 // 2
        self.process = None
        # Enable detailed per-frame debug logging
        self.debug = debug

    def _check_existing(self):
        # Check if any rpicam-vid process is already running
        result = subprocess.run(["pgrep", "-f", "rpicam-vid"], capture_output=True, text=True)
        if result.stdout.strip():
            for pid in result.stdout.strip().split("\n"):
                logging.warning(f"[CAMERA] rpicam-vid already running with PID={pid}. If safe, run: kill {pid}")
            return True
        return False

    def __enter__(self):
        # Check for existing camera processes before starting
        if self._check_existing():
            return self
        # Start camera via rpicam-vid piping raw YUV420 frames to stdout
        cam_cmd = [
            "rpicam-vid", "-t", "0", "--codec", "yuv420",
            "--width", str(self.width), "--height", str(self.height),
            "--framerate", str(self.fps), "--mode", "2304:1296:12:P",
            "--vflip", "--hflip", "-o", "-", "--nopreview"
        ]
        # Launch camera as a child process, read frames from stdout pipe
        self.process = subprocess.Popen(cam_cmd, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL)
        logging.info(f"[CAMERA] Started {self.width}x{self.height} @ {self.fps}fps")
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        # Always terminate camera process on exit, even on error
        if self.process is not None:
            self.process.terminate()
            self.process.wait()
            logging.info("[CAMERA] Stopped")

    def read_frame(self):
        # Guard against reading from a non-existent process
        if self.process is None:
            logging.error("[CAMERA] No camera process running")
            return None
        # Read raw bytes from pipe
        raw = self.process.stdout.read(self.frame_size)
        if len(raw) < self.frame_size:
            return None
        # Convert bytes to numpy array in YUV420 shape
        yuv = np.frombuffer(raw, dtype=np.uint8).reshape((self.height * 3 // 2, self.width))
        # Convert YUV420 to RGB
        rgb = cv2.cvtColor(yuv, cv2.COLOR_YUV2RGB_I420)
        if self.debug:
            logging.debug(f"[CAMERA] rgb shape: {rgb.shape} dtype: {rgb.dtype}")
        return rgb
