"""
Pipeline completo de deteção de faixas de rodagem para condução autónoma.
 
Fluxo principal:
  1. Câmara (ou imagem) → pré-processamento
  2. Inferência na Hailo-8 (acelerador NPU) com modelo YOLO26-seg
  3. Pós-processamento → máscara binária das faixas
  4. Bird's-Eye View (BEV) → vista de cima da estrada
  5. Sliding Windows → deteção e ajuste polinomial das linhas
  6. CTE (Cross-Track Error) → erro lateral do veículo em relação ao centro
  7. PID → cálculo do ângulo de direção
  8. CAN Bus → envio do comando de direção para o veículo
"""

import sys
import os
import cv2
import time
import argparse
import subprocess
import numpy as np

from core.hailo_engine import HailoEngine
from post_processing.yolo_decoder import YoloSegDecoder
from post_processing.mask_filters import MaskFilters
from LFA.geometry.bev_transform import BEVTransform
from LFA.geometry.sliding_windows import SlidingWindowsLaneFitter
from LFA.tracking.lane_identity_tracker import LaneIdentityTracker
from LFA.visualization.lane_visualiser import draw_lane_overlay, draw_text_overlay

try:
    from decision.PID_steering import PID
    from utils.can_sender import CanSender
except ImportError:
    print("Warning: Decision/can modules not found or with import error.")
    class PID:
        def __init__(self, *args): pass
        def update(self, _, cte, dt): return cte * 0.5
    class CanSender:
        def send_steering_percent(self, *args): pass
        def close(self): pass

CAM_WIDTH, CAM_HEIGHT, CAM_FPS = 640, 360, 30
DISPLAY_WIDTH, DISPLAY_HEIGHT = 1260, 400

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("mode", choices=["image", "camera"], help="Mode of execution")
    parser.add_argument("target", nargs="?", default="yolo26n_seg_640.hef", help="Path to HEF (if camera) or image (if image)")
    parser.add_argument("hef_or_thresh", nargs="?", default="0.25", help="Path to HEF (if image) or Threshold")
    parser.add_argument("threshold", nargs="?", default="0.25", help="Threshold")
    parser.add_argument("--remote", action="store_true")
    parser.add_argument("--no-display", action="store_true")
    args = parser.parse_args()

    if args.mode == "camera":
        hef_path = args.target
        threshold = float(args.hef_or_thresh)
    else:
        image_path = args.target
        hef_path = args.hef_or_thresh
        threshold = float(args.threshold)

    # 1. Setup Instâncias
    decoder = YoloSegDecoder(score_threshold=threshold)
    mask_filters = MaskFilters()
    # O PID ajusta o volante com base no erro lateral (CTE):
    #   Kp = ganho proporcional (reação imediata ao erro)
    #   Ki = ganho integral     (corrige erros acumulados ao longo do tempo)
    #   Kd = ganho derivativo   (suaviza oscilações prevendo a tendência do erro)
    #  !!! (kp, ki, kd) alterar aqui
    pid = PID(1.2, 0.4, 0.35)
    can = CanSender()
    bev = BEVTransform(CAM_WIDTH, CAM_HEIGHT)
    fitter = SlidingWindowsLaneFitter(cam_height=CAM_HEIGHT)
    tracker = LaneIdentityTracker(CAM_WIDTH, CAM_HEIGHT)

    # 2. Execução
    with HailoEngine(hef_path) as engine:
        print("Model Loaded. Engine Ready.")

        if args.mode == "image":
            bgr = cv2.imread(image_path)
            t0 = time.perf_counter()
            outputs = engine.infer(bgr)
            inf_ms = (time.perf_counter() - t0) * 1000

            binary_mask = decoder.decode_to_mask(outputs, CAM_HEIGHT, CAM_WIDTH)
            clean_mask = mask_filters.process(binary_mask)
            bev_mask = bev.warp(clean_mask)
            fit_raw = fitter.fit(bev_mask)
            
            # Ajuste p/ Virtual Lanes
            left_final = fit_raw.left_fit
            right_final = fit_raw.right_fit
            is_l_virt, is_r_virt = False, False
            if fitter.tracked_lane_width_px is not None:
                if left_final is None and right_final is not None:
                    left_final = right_final.copy()
                    left_final[2] -= fitter.tracked_lane_width_px
                    is_l_virt = True
                elif right_final is None and left_final is not None:
                    right_final = left_final.copy()
                    right_final[2] += fitter.tracked_lane_width_px
                    is_r_virt = True
            
            fit_raw.left_fit = left_final
            fit_raw.right_fit = right_final
            fit_raw.left_is_virtual = is_l_virt
            fit_raw.right_is_virtual = is_r_virt
            _, cte_n = fitter._calculate_cte(left_final, right_final, CAM_WIDTH, CAM_HEIGHT)
            fit_raw.cte_norm = cte_n

            if cte_n is not None:
                steer = pid.update(0.0, cte_n, 0.1)
                can.send_steering_percent(0x110, steer)

            res = draw_lane_overlay(bgr, fit_raw, bev)
            res = draw_text_overlay(res, fit_raw, inf_ms=inf_ms)
            cv2.imwrite("result_refactored.jpg", res)
            print("Processed image saved as result_refactored.jpg")

        elif args.mode == "camera":
            print(f"Starting camera ({CAM_WIDTH}x{CAM_HEIGHT} @ {CAM_FPS}fps)...")
            cam_cmd = [
                "rpicam-vid", "-t", "0", "--codec", "yuv420",
                "--width", str(CAM_WIDTH), "--height", str(CAM_HEIGHT),
                "--framerate", str(CAM_FPS), "--mode", "2304:1296:12:P",
                "--vflip", "--hflip", "-o", "-", "--nopreview"
            ]
            camera = subprocess.Popen(cam_cmd, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL)

            if args.remote or args.no_display:
                display = None
            else:
                gst_env = dict(os.environ, XDG_RUNTIME_DIR="/run/user/200", WAYLAND_DISPLAY="wayland-1")
                gst_cmd = (
                    f"gst-launch-1.0 fdsrc ! rawvideoparse format=bgr "
                    f"width={DISPLAY_WIDTH} height={DISPLAY_HEIGHT} framerate={CAM_FPS}/1 ! "
                    f"videoconvert ! queue ! waylandsink sync=false"
                )
                display = subprocess.Popen(gst_cmd, stdin=subprocess.PIPE, env=gst_env, shell=True)

            raw_frame_size = CAM_WIDTH * CAM_HEIGHT * 3 // 2
            
            frame_count = 0
            t_start = time.perf_counter()
            last_time = t_start
            last_valid_pid = 0.0

            try:
                while True:
                    raw = camera.stdout.read(raw_frame_size)
                    if len(raw) < raw_frame_size: break
                    yuv = np.frombuffer(raw, dtype=np.uint8).reshape((CAM_HEIGHT * 3 // 2, CAM_WIDTH))
                    bgr = cv2.cvtColor(yuv, cv2.COLOR_YUV2BGR_I420)

                    fitter.set_steering_hint(last_valid_pid)

                    t0 = time.perf_counter()
                    outputs = engine.infer(bgr)
                    inf_ms = (time.perf_counter() - t0) * 1000

                    binary_mask = decoder.decode_to_mask(outputs, CAM_HEIGHT, CAM_WIDTH)
                    clean_mask = mask_filters.process(binary_mask)
                    bev_mask = bev.warp(clean_mask)
                    fit_raw = fitter.fit(bev_mask)

                    # Virtual Lanes / CTE
                    left_final = fit_raw.left_fit
                    right_final = fit_raw.right_fit
                    is_l_virt, is_r_virt = False, False
                    if fitter.tracked_lane_width_px is not None:
                        if left_final is None and right_final is not None:
                            left_final = right_final.copy()
                            left_final[2] -= fitter.tracked_lane_width_px
                            is_l_virt = True
                        elif right_final is None and left_final is not None:
                            right_final = left_final.copy()
                            right_final[2] += fitter.tracked_lane_width_px
                            is_r_virt = True
                            
                    fit_raw.left_fit = left_final
                    fit_raw.right_fit = right_final
                    fit_raw.left_is_virtual = is_l_virt
                    fit_raw.right_is_virtual = is_r_virt
                    _, cte_n = fitter._calculate_cte(left_final, right_final, CAM_WIDTH, CAM_HEIGHT)
                    fit_raw.cte_norm = cte_n

                    frame_count += 1
                    fps = frame_count / (time.perf_counter() - t_start)
                    current_time = time.perf_counter()
                    dt = current_time - last_time
                    last_time = current_time

                    cte = fit_raw.cte_norm if fit_raw.cte_norm is not None else 0.0
                    pid_return = pid.update(0.0, cte, dt)
                    if abs(last_valid_pid - pid_return) <= 0.4:
                        can.send_steering_percent(0x110, pid_return * (-1))
                    last_valid_pid = pid_return

                    if not args.no_display:
                        res = draw_lane_overlay(bgr, fit_raw, bev)
                        display_frame = cv2.resize(res, (DISPLAY_WIDTH, DISPLAY_HEIGHT))
                        display_frame = draw_text_overlay(display_frame, fit_raw, fps=fps, inf_ms=inf_ms)
                        
                        if args.remote:
                            _, buf = cv2.imencode('.jpg', display_frame, [cv2.IMWRITE_JPEG_QUALITY, 80])
                            sys.stdout.buffer.write(buf.tobytes())
                            sys.stdout.buffer.flush()
                        elif display is not None:
                            display.stdin.write(display_frame.tobytes())
                            display.stdin.flush()

            except KeyboardInterrupt:
                print("\nShutting down...")
            finally:
                camera.terminate()
                can.close()

if __name__ == "__main__":
    main()