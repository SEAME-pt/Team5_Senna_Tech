#!/usr/bin/env python3
import cv2
import numpy as np
import os
import subprocess
import time

from hailo_platform import (
    ConfigureParams,
    HEF,
    HailoStreamInterface,
    InferVStreams,
    InputVStreamParams,
    OutputVStreamParams,
    VDevice,
)

# ---------------------------------------------------------------
# Configuration Class
# ---------------------------------------------------------------
class Config:
    """Stores all script configuration values."""
    def __init__(self, hef_path='yolov8s_seg.hef'):
        self.HEF_PATH = self._find_hef(hef_path)
        self.NET_WIDTH, self.NET_HEIGHT = 640, 640

        # --- POST-PROCESSING CONFIGURATION (Fixed values) ---
        self.SCORE_THRESHOLD = 0.25
        self.IOU_THRESHOLD = 0.7
        self.META_ARCH = "yolov8"
        print(f"Internal configuration: Score>={self.SCORE_THRESHOLD}, IoU>={self.IOU_THRESHOLD}")
        # ---------------------------------------------------------

        self.CAM_WIDTH, self.CAM_HEIGHT = 640, 640
        self.CAM_FRAMERATE = 30
        self.CLASSES = ["pista"]
        self.NUM_CLASSES = len(self.CLASSES)
        self.MASK_COLORS = np.array([[100, 255, 100]], dtype=np.uint8)

    def _find_hef(self, hef_path):
        """Search for the HEF in common locations on the target device."""
        home_path = os.path.join('/home', os.path.basename(hef_path))
        if os.path.exists(home_path): return home_path
        if os.path.exists(hef_path): return hef_path
        if os.path.exists(os.path.basename(hef_path)): return os.path.basename(hef_path)
        raise FileNotFoundError(f"HEF file '{hef_path}' not found in /home/ or the current directory.")

# ---------------------------------------------------------------
# YOLOv8-Seg Post-processing Class (Final Version)
# ---------------------------------------------------------------
class YoloV8SegPost:
    """Simplified post-processing for YOLOv8-Seg lane detection.
    Uses scores, mask coefficients, and the prototype only. No bounding boxes."""
    def __init__(self, config: Config):
        self.config = config
        self.net_h, self.net_w = config.NET_HEIGHT, config.NET_WIDTH

    def __call__(self, outputs, original_shape):
        """Generate the lane segmentation mask directly."""
        # 1. Find the prototype tensor (160x160x32)
        try:
            proto_key = next(k for k, v in outputs.items() if len(v.shape) == 4 and v.shape[1] == 160)
            proto = outputs[proto_key][0]  # (160, 160, 32)
            if proto.shape[-1] == 32:
                proto = np.transpose(proto, (2, 0, 1))  # (32, 160, 160)
        except StopIteration:
            return None

        # 2. Collect scores and mask coefficients across all scales
        all_scores = []
        all_mask_coeffs = []
        for stride in [8, 16, 32]:
            h, w = self.net_h // stride, self.net_w // stride
            try:
                score_key = next(k for k,v in outputs.items() if v.shape == (1,h,w,self.config.NUM_CLASSES))
                mask_key = next(k for k,v in outputs.items() if v.shape == (1,h,w,32))
            except StopIteration:
                continue
            all_scores.append(outputs[score_key][0].reshape(-1))
            all_mask_coeffs.append(outputs[mask_key][0].reshape(-1, 32))

        if not all_scores:
            return None

        scores = np.concatenate(all_scores)
        mask_coeffs = np.vstack(all_mask_coeffs).astype(np.float32)

        # 3. Keep only the top-K most confident anchors
        top_k = min(50, len(scores))
        top_indices = np.argpartition(scores, -top_k)[-top_k:]
        top_scores = scores[top_indices]

        # Filter by confidence
        valid = top_scores > self.config.SCORE_THRESHOLD
        if not np.any(valid):
            return None

        top_scores = top_scores[valid]
        top_coeffs = mask_coeffs[top_indices[valid]]

        # 4. Generate a score-weighted mask: (scores @ coeffs) @ proto -> sigmoid
        # Weighted average of coefficients by score -> a single vector of 32 coefficients
        weights = top_scores / top_scores.sum()
        weighted_coeffs = (weights[:, None] * top_coeffs).sum(axis=0, keepdims=True)  # (1, 32)

        proto_flat = proto.reshape(32, -1).astype(np.float32)  # (32, 25600)
        raw = weighted_coeffs @ proto_flat  # (1, 25600)
        combined = 1 / (1 + np.exp(-np.clip(raw, -30, 30)))  # sigmoid
        combined = combined.reshape(proto.shape[1], proto.shape[2])  # (160, 160)

        # 6. Resize to the original frame size
        combined = cv2.resize(combined, (original_shape[1], original_shape[0]))
        return (combined > 0.5).astype(np.uint8)

# ---------------------------------------------------------------
# Drawing and System Functions
# ---------------------------------------------------------------
def draw_results(frame, mask, config: Config):
    if mask is not None and mask.any():
        # Color the lane area
        overlay = frame.copy()
        overlay[mask == 1] = config.MASK_COLORS[0]
        frame = cv2.addWeighted(overlay, 0.4, frame, 0.6, 0)

        # Draw the lane border lines
        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        cv2.drawContours(frame, contours, -1, (0, 255, 0), 2)
    return frame

def read_system_stats():
    try: return int(open("/sys/class/hwmon/hwmon0/temp1_input").read()) / 1000.0
    except Exception: return 0.0

# ---------------------------------------------------------------
# Main Inference Class
# ---------------------------------------------------------------
class HailoInference:
    def __init__(self, config: Config):
        self.config, self.post_processor = config, YoloV8SegPost(config)
        self.hef = HEF(config.HEF_PATH)
        print(f"HEF model loaded from: {config.HEF_PATH}")

    def run(self):
        camera, display = self._start_camera(), self._start_display()
        try:
            with VDevice() as target:
                configure_params = ConfigureParams.create_from_hef(self.hef, interface=HailoStreamInterface.PCIe)
                network_group = target.configure(self.hef, configure_params)[0]
                with network_group.activate(network_group.create_params()):
                    input_vstream_params = InputVStreamParams.make(network_group)
                    output_vstream_params = OutputVStreamParams.make(network_group)
                    with InferVStreams(network_group, input_vstream_params, output_vstream_params) as pipeline:
                        self._inference_loop(camera, display, pipeline, input_vstream_params)
        except KeyboardInterrupt: print("Stopped by user.")
        except Exception as e: print(f"FATAL ERROR: {e}")
        finally:
            print("Shutting down processes...")
            if camera: camera.terminate()
            if display: display.terminate()
            print("System shutdown complete.")

    def _start_camera(self):
        print("Starting camera...")
        cmd = ["rpicam-vid", "-t", "0", "--codec", "yuv420", "--width", str(self.config.CAM_WIDTH),
               "--height", str(self.config.CAM_HEIGHT), "--framerate", str(self.config.CAM_FRAMERATE),
               "--vflip", "--hflip", "-o", "-", "--nopreview"]
        return subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL)

    def _start_display(self):
        print("Starting display...")
        gst_env = dict(os.environ, XDG_RUNTIME_DIR="/run/user/200", WAYLAND_DISPLAY="wayland-1")
        cmd = (f"gst-launch-1.0 fdsrc ! rawvideoparse format=bgr width={self.config.CAM_WIDTH} "
               f"height={self.config.CAM_HEIGHT} framerate={self.config.CAM_FRAMERATE}/1 ! "
               f"videoconvert ! waylandsink")
        return subprocess.Popen(cmd, stdin=subprocess.PIPE, env=gst_env, shell=True)

    def _inference_loop(self, camera, display, pipeline, input_params):
        input_name = list(input_params.keys())[0]
        raw_frame_size = self.config.CAM_WIDTH * self.config.CAM_HEIGHT * 3 // 2
        frame_count, start_time = 0, time.time()
        print("System ready. Running inference. Press Ctrl+C to stop.")

        while True:
            raw_frame = camera.stdout.read(raw_frame_size)
            if len(raw_frame) < raw_frame_size: break

            yuv_frame = np.frombuffer(raw_frame, dtype=np.uint8).reshape((self.config.CAM_HEIGHT * 3 // 2, self.config.CAM_WIDTH))
            bgr_frame = cv2.cvtColor(yuv_frame, cv2.COLOR_YUV2BGR_I420)

            input_data = {input_name: np.expand_dims(cv2.cvtColor(bgr_frame, cv2.COLOR_BGR2RGB), axis=0)}

            outputs = pipeline.infer(input_data)

            mask = self.post_processor(outputs, bgr_frame.shape)

            result_frame = draw_results(bgr_frame.copy(), mask, self.config)

            frame_count += 1
            fps = frame_count / (time.time() - start_time)
            temp = read_system_stats()
            cv2.putText(result_frame, f"FPS: {fps:.1f}", (10, 25), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
            cv2.putText(result_frame, f"Temp: {temp:.1f}C", (10, 55), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 200, 255), 2)
            if mask is not None and mask.any(): cv2.putText(result_frame, "Lane OK", (10, 85), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 200, 0), 2)

            display.stdin.write(result_frame.tobytes())
            display.stdin.flush()

# ---------------------------------------------------------------
# Entry Point
# ---------------------------------------------------------------
if __name__ == '__main__':
    print('--- Starting TSHailo - Segmentation Post-processing (Senna Edition) ---')
    try:
        config = Config(hef_path='yolov8n_seg.hef')
        inference_manager = HailoInference(config)
        inference_manager.run()
    except Exception as e:
        print(f"Startup failed. ERROR: {e}")
