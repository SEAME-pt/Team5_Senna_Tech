"""
Complete lane departure detection pipeline for autonomous driving.

Main flow:
1. Camera (or image) → pre-processing
2. Inference on the Hailo-8 (NPU accelerator) with YOLO26-sec model
3. Post-processing → binary lane masking
4. Bird's-Eye View (BEV) → top-down view of the road
5. Sliding Windows → polynomial line detection and adjustment
6. CTE (Cross-Track Error) → lateral error of the vehicle relative to the center
7. PID → steering angle calculation
8. CAN Bus → sending steering commands to the vehicle
"""

import sys
import os
import cv2
import time
import argparse
import subprocess
import numpy as np
import logging
#para debug, apagar depois
logging.basicConfig(level=logging.INFO)

from object.ObjectDetector import ObjectDetector
from core.hailo_engine import HailoEngine
from core.hailo_engine import VDevice
from post_processing.yolo_decoder import YoloSegDecoder
from post_processing.mask_filters import MaskFilters
from LFA.geometry.bev_transform import BEVTransform
from LFA.geometry.sliding_windows import SlidingWindowsLaneFitter
from LFA.visualization.lane_visualiser import draw_lane_overlay, draw_text_overlay
from object.perception_objects import EnvironmentState, Detection, ClassID, ObstacleSituation
from decision.decision_fsm import VehicleFSM, State, AVOIDANCE_STATES
from decision.path_planner import PathPlanner
from object.obstacle_tracker import ObstacleTracker
from object.perception_objects import EnvironmentState, Detection, ClassID
from object.corridor_check import CorridorChecker
from kuksa_publish.kuksa_publish import KuksaClient
from decision.adaptive_cruise import AdaptiveCruiseControl

try:
    from decision.PID_steering import PID
    from utils.can_sender import CanSender
except ImportError:
    print("Warning: Decision/can modules not found or with import error.")
    class PID:
        def __init__(self, *args): pass
        def update(self, _, cte, dt): return cte * 0.5
    class CanSender:
        def send_can_percent(self, *args): pass
        def send_fsm_state(self, *args): pass
        def close(self): pass

CAM_WIDTH, CAM_HEIGHT, CAM_FPS = 640, 360, 60
DISPLAY_WIDTH, DISPLAY_HEIGHT = 1260, 400

STATE_THROTTLE = {
    State.EMERGENCY:     200, # abstract value to represent emergency break on the microcontroller
    State.STOP:          0,
    State.SPEED_SLOW:    5,
    State.SPEED_50:      8,
    State.SPEED_80:      10,
    State.FOLLOW:        0,   # ACC
    State.PREPARE_AVOID: 5,
    State.AVOIDING:      5,
    State.BLIND_WAIT:    5,
    State.RETURNING:     5,
}

def main():
    parser = argparse.ArgumentParser()

    # dois modelos obrigatórios
    parser.add_argument("lane", help="Path to Lane Detection model")
    parser.add_argument("object", help="Path to Object Detection model")

    # Display flags
    parser.add_argument("--remote", action="store_true")
    parser.add_argument("--no-display", action="store_true")
    parser.add_argument("--virtual", action="store_true") ## To not move servo motor
    args = parser.parse_args()

    lane_hef_path = args.lane   # get lane .hef path
    obj_hef_path = args.object   # get object .hef path

    # Init useful instancies
    threshold = 0.25
    decoder = YoloSegDecoder(score_threshold=threshold)
    detector = ObjectDetector()
    mask_filters = MaskFilters()
    #  !!! (kp, ki, kd) alterar aqui
    pid = PID(0.9, 0.2, 0.6)
    can = CanSender(channel="can0")
    bev = BEVTransform(CAM_WIDTH, CAM_HEIGHT)
    fitter = SlidingWindowsLaneFitter(cam_height=CAM_HEIGHT)
    kuksa_channel = KuksaClient()
    checker = CorridorChecker(bev)
    fsm = VehicleFSM()
    planner      = PathPlanner(
        lane_offset       = 0.80,   # ~65 px in 170 px road width
        blind_wait_time   = 2.5,    # seconds in BLIND_WAIT
        return_duration_s = 1.5,    # return interpolation duration
    )
    obs_tracker  = ObstacleTracker(
        area_brake_threshold = 0.060,# area delta in a frame that triggers BRAKE
        area_avoidance_min   = 0.010,# minimum area for counting avoidance frames
        frames_to_confirm    = 4, # frames in tracker before reporting AVOIDANCE
        frame_width_bev      = CAM_WIDTH,
    )
    adaptive_cruise = AdaptiveCruiseControl()

    with VDevice() as target: # Get Hailo Device and define as 'target'
        with HailoEngine(lane_hef_path, target) as engine_lane, \
            HailoEngine(obj_hef_path, target) as engine_obj:

            print("Models Loaded. Engines Ready.")

            print(f"Starting camera ({CAM_WIDTH}x{CAM_HEIGHT} @ {CAM_FPS}fps)...")

            cam_cmd = [
                "rpicam-vid", "-t", "0", "--codec", "yuv420",
                "--width", str(CAM_WIDTH), "--height", str(CAM_HEIGHT),
                "--framerate", str(CAM_FPS), "--mode", "2304:1296:8:P", #"2304:1296:8:P"
                "--shutter", "5000", "--vflip", "--hflip", "-o", "-", "--nopreview"
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
            last_valid_state = 0

            # vars to avoid spamming commands when not necessary
            last_sent_throttle = None
            last_sent_steering = None

            try:
                while True:
                    t_frame_start = time.perf_counter()

                    # ==== CAMERA =====
                    t0 = time.perf_counter()

                    raw = camera.stdout.read(raw_frame_size)
                    if len(raw) < raw_frame_size:
                        break

                    yuv = np.frombuffer(raw, dtype=np.uint8).reshape((CAM_HEIGHT * 3 // 2, CAM_WIDTH))
                    bgr = cv2.cvtColor(yuv, cv2.COLOR_YUV2BGR_I420)

                    t_camera = (time.perf_counter() - t0) * 1000

                    # ==== INFERENCE ====
                    t0 = time.perf_counter() # START FPS COUNT

                    # RUN LANE MODEL 
                    outputs_lane = engine_lane.infer(bgr)

                    inf_lane_ms = (time.perf_counter() - t0) * 1000 # GET TIME TO RUN BOTH INFERENCES
                    t0 = time.perf_counter() # START FPS COUNT
                    
                    # RUN OBJECT MODEL
                    outputs_obj = engine_obj.infer(bgr)
                    inf_obj_ms = (time.perf_counter() - t0) * 1000 # GET TIME TO RUN BOTH INFERENCES

                    # ==== LANE PIPELINE POST PROCESS ======
                    t0 = time.perf_counter() # START FPS COUNT
                    binary_mask = decoder.decode_to_mask(outputs_lane, CAM_HEIGHT, CAM_WIDTH)
                    clean_mask = mask_filters.process(binary_mask)
                    bev_mask = bev.warp(clean_mask)
                    fit_result = fitter.fit(bev_mask)

                    # ==== OBJECT ======
                    detections = detector.process(outputs_obj, bgr.shape)
                    #bgr = detector.draw(bgr, detections) # draw detections on frame

                    env_state = EnvironmentState(detections=[], corridor_clear=True)
                    env_state.lead_car_detected = False
                    env_state.lead_car_area     = 0.0

                    for det_dict in detections:
                        db_info = checker.check_and_debug(det_dict["bbox"], fit_result, bgr.shape)
                        in_corridor = db_info["in_corridor"]
                        rel_area = db_info["rel_area"]
                        
                        det_dict["in_corridor"] = in_corridor
                        det_dict["relative_area"] = rel_area
                        det_dict["debug_info"] = db_info

                        try:
                            cid = ClassID(det_dict["class_id"])
                        except ValueError:
                            continue

                        #d = Detection(class_id=cid, in_corridor=in_corridor, relative_area=rel_area)
                        #env_state.detections.append(d)
                        env_state.detections.append(
                            Detection(class_id=cid, in_corridor=in_corridor, relative_area=rel_area)
                        )
                        
                        # Detects either car or obstacle in corridor
                        if in_corridor and cid == ClassID.OBSTACLE:
                            env_state.corridor_clear = False

                        # If car is detected in the corridor, start adaptive cruise control
                        elif in_corridor and cid == ClassID.CAR:
                            env_state.corridor_clear = False
                            env_state.lead_car_detected = True
                            if rel_area > env_state.lead_car_area:
                                env_state.lead_car_area = rel_area

                    bgr = detector.draw(bgr, detections)

                    t_post = (time.perf_counter() - t0) * 1000
                    #enviar dados para kuksa (!!!! pendente de troca, colocar depois do can !!!!!)
                    t0 = time.perf_counter()
                    kuksa_channel.send(env_state.detections)
                    t_kuksa = (time.perf_counter() - t0) * 1000

                    # ===== OBSTACLE TRACKER ========
                    obs_info = obs_tracker.update(detections)

                    # ===== BLIND WAIT TIMER =======
                    if fsm.state == State.BLIND_WAIT:
                        if planner.check_blind_wait_timeout():
                            fsm.signal_blind_wait_timeout()
                            planner.reset_blind_timer()
                    else:
                        planner.reset_blind_timer()

                    # ==== FSM DECISION ====
                    """                     print("STATE: \n")
                    print(env_state)
                    print("ENV STATE. DETECTIONS: \n")
                    print(env_state.detections) """
                    t0 = time.perf_counter()
                    current_state = fsm.process(
                        env_state,
                        obstacle_situation = obs_info.situation,
                        planner_return_complete = planner.return_complete(),
                    )

                    if current_state not in AVOIDANCE_STATES:
                        obs_tracker.reset()

                    frame_count += 1

                    current_time = time.perf_counter()
                    dt = current_time - last_time
                    last_time = current_time

                    # ==== PID + CTE ====
                    cte_actual = fit_result.cte_norm if fit_result.cte_norm is not None else 0.0
                    target_cte = planner.calculate_target_cte(
                        current_state,
                        obstacle_side = obs_info.side,
                    )

                    pid_return = pid.update(target_cte, cte_actual, dt)
                    pid_return = round(pid_return, 2)

                    throttle = STATE_THROTTLE.get(current_state, 0)
                    if current_state == State.FOLLOW:
                        acc_value = adaptive_cruise.compute_follow_error(env_state.lead_car_area)
                        throttle = acc_value

                    # ===== CAN ====
                    if not args.virtual:
                        if throttle != last_sent_throttle:
                            can.send_int16(0x001, throttle)
                            last_sent_throttle = throttle

                    steering = round(pid_return * -1, 2)
                    if steering != last_sent_steering:
                        can.send_can_percent(0x110, steering)
                        last_sent_steering = steering

                    if last_valid_state is None or current_state.value != last_valid_state:
                        last_valid_state = current_state.value
                        print(f"NEW MODE: {current_state.name} | throttle={throttle}")

                    t_decision = (time.perf_counter() - t0) * 1000

                    fps = frame_count / (time.perf_counter() - t_start)
                    t0 = time.perf_counter()

                    # ==== DISPLAY ====
                    if not args.no_display:
                        res = draw_lane_overlay(bgr, fit_result, bev)
                        display_frame = cv2.resize(res, (DISPLAY_WIDTH, DISPLAY_HEIGHT))
                        #display_frame = draw_text_overlay(display_frame, fit_result, fps=fps, inf_ms=inf_ms)

                        if args.remote:
                            _, buf = cv2.imencode('.jpg', display_frame, [cv2.IMWRITE_JPEG_QUALITY, 80])
                            sys.stdout.buffer.write(buf.tobytes())
                            sys.stdout.buffer.flush()
                        elif display is not None:
                            display.stdin.write(display_frame.tobytes())
                            display.stdin.flush()

                    t_display = (time.perf_counter() - t0) * 1000
                    #print(
                    #    f"FPS: {fps:.1f} | "
                    #    f"Cam: {t_camera:.1f}ms | "
                    #    f"Lane model: {inf_lane_ms:.1f}ms | "
                    #    f"Obj model: {inf_obj_ms:.1f}ms | "
                    #    f"Post: {t_post:.1f}ms | "
                    #    f"Kuksa: {t_kuksa:.1f}ms | "
                    #    f"Decision: {t_decision:.1f}ms | "
                    #    f"Display: {t_display:.1f}ms | "
                    #)

            except KeyboardInterrupt:
                print("\nShutting down...")
            finally:
                camera.terminate()
                can.close()

if __name__ == "__main__":
    main()
