import os
import sys
import cv2
import subprocess
import logging


class Display:
    def __init__(self, width: int, height: int, fps: int, mode: str = "local"):
        self.width  = width
        self.height = height
        self.fps    = fps
        self.mode   = mode
        self._process = None

    def __enter__(self):
        if self.mode == "local":
            gst_env = dict(os.environ, XDG_RUNTIME_DIR="/run/user/200", WAYLAND_DISPLAY="wayland-1")
            gst_cmd = (
                f"gst-launch-1.0 fdsrc ! rawvideoparse format=rgb "
                f"width={self.width} height={self.height} framerate={self.fps}/1 ! "
                f"videoconvert ! queue ! waylandsink sync=false"
            )
            self._process = subprocess.Popen(gst_cmd, stdin=subprocess.PIPE, env=gst_env, shell=True)
            logging.info("[DISPLAY] Started local display %dx%d @ %dfps", self.width, self.height, self.fps)
        elif self.mode == "remote":
            logging.info("[DISPLAY] Started remote display (JPEG stdout)")
        return self

    def show(self, frame):
        if self.mode == "none":
            return

        display_frame = cv2.resize(frame, (self.width, self.height))

        if self.mode == "remote":
            _, buf = cv2.imencode('.jpg', display_frame, [cv2.IMWRITE_JPEG_QUALITY, 80])
            sys.stdout.buffer.write(buf.tobytes())
            sys.stdout.buffer.flush()

        elif self.mode == "local" and self._process is not None:
            self._process.stdin.write(display_frame.tobytes())
            self._process.stdin.flush()

    def close(self):
        if self._process is not None:
            self._process.terminate()
            self._process = None
            logging.info("[DISPLAY] Stopped")

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()
