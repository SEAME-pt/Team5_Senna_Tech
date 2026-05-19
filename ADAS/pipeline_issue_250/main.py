import argparse
import logging

logging.basicConfig(level=logging.INFO)

from camera import Camera
from inference import HailoEngine, VDevice
from post_processing import YoloSegDecoder, MaskFilters, ObjectDetector, CorridorChecker, build_environment_state, ObstacleTracker
from LFA import BEVTransform, SlidingWindowsLaneFitter, draw_lane_overlay
from decision import VehicleFSM, State, AVOIDANCE_STATES, STATE_THROTTLE, PathPlanner, AdaptiveCruiseControl, PID
from kuksa_publish import KuksaClient
from utils import CanSender, Display, Timer

try:
    from utils import CanSender, Display
except ImportError:
    class CanSender:
        def send_drive_command(self, *args): pass
        def close(self): pass
    class Display:
        def __init__(self, *args, **kwargs): pass
        def __enter__(self): return self
        def __exit__(self, *args): pass
        def show(self, frame): pass

CAM_WIDTH, CAM_HEIGHT, CAM_FPS = 640, 360, 15
DISPLAY_WIDTH, DISPLAY_HEIGHT = 1260, 400


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("lane",   help="Path to Lane Detection HEF model")
    parser.add_argument("object", help="Path to Object Detection HEF model")
    parser.add_argument("--remote",     action="store_true", help="Enable remote display streaming")
    parser.add_argument("--no-display", action="store_true", help="Disable display output")
    parser.add_argument("--virtual",    action="store_true", help="Enable virtual mode (no physical CAN commands)")
    args = parser.parse_args()

    decoder        = YoloSegDecoder(score_threshold=0.25)
    mask_filters   = MaskFilters()
    detector       = ObjectDetector()
    pid            = PID(1.3, 0.1, 0.1)
    can            = CanSender(channel="can0")
    bev            = BEVTransform(CAM_WIDTH, CAM_HEIGHT)
    fitter         = SlidingWindowsLaneFitter(cam_height=CAM_HEIGHT)
    kuksa_channel  = KuksaClient()
    checker        = CorridorChecker(bev)
    fsm            = VehicleFSM()
    planner        = PathPlanner(
        lane_offset       = 0.80,
        blind_wait_time   = 2.5,
        return_duration_s = 1.5,
    )
    obs_tracker    = ObstacleTracker(
        area_brake_threshold = 0.060,
        area_avoidance_min   = 0.010,
        frames_to_confirm    = 4,
        frame_width_bev      = CAM_WIDTH,
    )
    adaptive_cruise = AdaptiveCruiseControl()

    if args.remote:
        display_mode = "remote"
    elif args.no_display:
        display_mode = "none"
    else:
        display_mode = "local"

    with VDevice() as target:
        with HailoEngine(args.lane, target) as engine_lane, \
             HailoEngine(args.object, target) as engine_obj, \
             Camera(CAM_WIDTH, CAM_HEIGHT, CAM_FPS) as cam, \
             Display(DISPLAY_WIDTH, DISPLAY_HEIGHT, CAM_FPS, mode=display_mode) as display:

            logging.info("Models loaded. Engines ready.")

            try:
                while True:
                    t_loop_start = Timer.start_loop()

                    # ── CAMERA ──────────────────────────────────────────
                    Timer.start_stage("Camera")
                    rgb = cam.get_frame()
                    if rgb is None:
                        continue
                    Timer.end_stage("Camera")

                    # ── INFERENCE ────────────────────────────────────────
                    Timer.start_stage("Inf_Lane")
                    outputs_lane = engine_lane.infer(rgb)
                    Timer.end_stage("Inf_Lane")

                    Timer.start_stage("Inf_Obj")
                    outputs_obj  = engine_obj.infer(rgb)
                    Timer.end_stage("Inf_Obj")

                    # ── LANE POST-PROCESSING ─────────────────────────────
                    Timer.start_stage("Post")
                    binary_mask = decoder.decode_to_mask(outputs_lane, CAM_HEIGHT, CAM_WIDTH)
                    clean_mask  = mask_filters.process(binary_mask)
                    bev_mask    = bev.warp(clean_mask)
                    fit_result  = fitter.fit(bev_mask)

                    # ── OBJECT DETECTION ─────────────────────────────────
                    detections = detector.process(outputs_obj, rgb.shape)
                    env_state  = build_environment_state(detections, fit_result, checker, rgb.shape)
                    rgb = detector.draw(rgb, detections)
                    Timer.end_stage("Post")

                    # ── KUKSA ────────────────────────────────────────────
                    Timer.start_stage("Kuksa")
                    kuksa_channel.send(env_state.detections)
                    Timer.end_stage("Kuksa")

                    # ── OBSTACLE TRACKER ─────────────────────────────────
                    obs_info = obs_tracker.update(detections)

                    # ── BLIND WAIT TIMER ─────────────────────────────────
                    if fsm.state == State.BLIND_WAIT:
                        if planner.check_blind_wait_timeout():
                            fsm.signal_blind_wait_timeout()
                            planner.reset_blind_timer()
                    else:
                        planner.reset_blind_timer()

                    # ── FSM DECISION ─────────────────────────────────────
                    Timer.start_stage("Decision")
                    current_state = fsm.process(
                        env_state,
                        obstacle_situation      = obs_info.situation,
                        planner_return_complete = planner.return_complete(),
                    )
                    if current_state not in AVOIDANCE_STATES:
                        obs_tracker.reset()

                    # ── PID + CTE ────────────────────────────────────────
                    cte_actual = fit_result.cte_norm if fit_result.cte_norm is not None else 0.0
                    target_cte = planner.calculate_target_cte(
                        current_state,
                        obstacle_side = obs_info.side,
                    )
                    pid_return = round(pid.update(target_cte, cte_actual, 0.1), 2) # simplified dt for now
                    throttle = STATE_THROTTLE.get(current_state, 0)
                    if current_state == State.FOLLOW:
                        throttle = adaptive_cruise.compute_follow_error(env_state.lead_car_area)

                    # ── CAN ──────────────────────────────────────────────
                    steering = round(pid_return * -1, 2)
                    if not args.virtual:
                        if throttle != last_sent_throttle or steering != last_sent_steering:
                            can.send_drive_command(0x002, throttle, steering)
                            last_sent_throttle = throttle
                            last_sent_steering = steering

                    if last_valid_state is None or current_state.value != last_valid_state:
                        last_valid_state = current_state.value
                        logging.info("NEW MODE: %s | throttle=%s", current_state.name, throttle)

                    Timer.end_stage("Decision")

                    # ── DISPLAY ──────────────────────────────────────────
                    Timer.start_stage("Display")
                    if display_mode != "none":
                        res = draw_lane_overlay(rgb, fit_result, bev)
                        display.show(res)
                    Timer.end_stage("Display")

                    fps = Timer.get_fps()
                    cpu_temp = Timer.read_temp()
                    total_cycle_time = Timer.end_loop()

                    logging.info(
                        "FPS: %.1f | Temp: %.1fC | Cycle: %.1fms | %s",
                        fps, cpu_temp, total_cycle_time, Timer.get_report(),
                    )

            except KeyboardInterrupt:
                logging.info("Shutting down...")
            finally:
                cam.stop()
                can.close()


if __name__ == "__main__":
    main()
