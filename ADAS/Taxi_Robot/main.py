import argparse
import logging

from map.track_map import (
    get_aruco_id, parse_coord, validate_coord, 
    PARKING_ARUCO_ID, PARKING_POS,
)

from map.path import print_path_map
from decision.robotaxi_mission import RobotaxiMission, TaxiManeuver

logging.basicConfig(level=logging.INFO)

from camera import Camera
from inference import HailoEngine, VDevice
from post_processing import YoloSegDecoder, MaskFilters, ObjectDetector
from object import CorridorChecker, build_environment_state, ObstacleTracker
from LFA import BEVTransform, SlidingWindowsLaneFitter, draw_lane_overlay
from decision import VehicleFSM, State, AVOIDANCE_STATES, STATE_THROTTLE, TAXIROBOT_STATES, PathPlanner, AdaptiveCruiseControl, PID
from kuksa_publish import KuksaClient
from utils import CanSender, Display, HardwareMonitor, Timer
from localization import ArucoWorker

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

    parser.add_argument("lane",   help="Path to Lane Detection HEF model") # get lane .hef path
    parser.add_argument("object", help="Path to Object Detection HEF model")  # get object .hef path

    parser.add_argument("pickup", help="Pickup position. Format: row,col")
    parser.add_argument("dropoff", help="Drop-off position. Format: row,col")

    parser.add_argument("--remote",     action="store_true", help="Enable remote display streaming")
    parser.add_argument("--no-display", action="store_true", help="Disable display output")
    parser.add_argument("--virtual",    action="store_true", help="Enable virtual mode (no physical CAN commands)")  ## To not move servo motor

    args = parser.parse_args()

    # ── TAXI ROBOT ARGUMENTS VALIDATION ─────────────────────────────────
    pickup = parse_coord(args.pickup)
    dropoff = parse_coord(args.dropoff)

    validate_coord("pickup", pickup)
    validate_coord("dropoff", dropoff)

    pickup_aruco_id = get_aruco_id(pickup)
    dropoff_aruco_id = get_aruco_id(dropoff)

    if pickup_aruco_id is None:
        raise ValueError(
            f"pickup {pickup} must be on an ArUco marker cell"
        )

    if dropoff_aruco_id is None:
        raise ValueError(
            f"dropoff {dropoff} must be on an ArUco marker cell"
        )

    if pickup == PARKING_POS:
        raise ValueError("pickup cannot be the parking position")

    if dropoff == PARKING_POS:
        raise ValueError("dropoff cannot be the parking position")

    robotaxi = RobotaxiMission(
        parking=PARKING_POS,
        pickup=pickup,
        dropoff=dropoff,
        parking_aruco_id=PARKING_ARUCO_ID,
        pickup_aruco_id=pickup_aruco_id,
        dropoff_aruco_id=dropoff_aruco_id,
    )

    current_grid_pos = PARKING_POS

    logging.info("Robotaxi enabled")
    logging.info("Parking    : %s", PARKING_POS)
    logging.info("Pickup     : %s", pickup)
    logging.info("Dropoff    : %s", dropoff)

    decoder        = YoloSegDecoder(score_threshold=0.25)
    mask_filters   = MaskFilters()
    detector       = ObjectDetector()
    pid            = PID(1.3, 0.1, 0.1)
    can            = CanSender(channel="can0")
    bev            = BEVTransform(CAM_WIDTH, CAM_HEIGHT)
    fitter         = SlidingWindowsLaneFitter(cam_height=CAM_HEIGHT)
    kuksa_channel  = KuksaClient()
    aruco_worker = ArucoWorker(frequency_hz=5)
    aruco_worker.start()
    checker        = CorridorChecker(bev)
    fsm            = VehicleFSM()
    planner        = PathPlanner(
        lane_offset       = 0.80,   # ~65 px in 170 px road width
        blind_wait_time   = 2.5,    # seconds in BLIND_WAIT
        return_duration_s = 1.5,    # return interpolation duration
    )
    obs_tracker    = ObstacleTracker(
        area_brake_threshold = 0.060,   # area delta in a frame that triggers BRAKE
        area_avoidance_min   = 0.010,   # minimum area to consider for avoidance
        frames_to_confirm    = 4,       # frames in tracker before reporting AVOIDANCE
        frame_width_bev      = CAM_WIDTH,
    )
    adaptive_cruise = AdaptiveCruiseControl()
    hw_monitor      = HardwareMonitor()
    timer           = Timer()

    if args.remote:
        display_mode = "remote"
    elif args.no_display:
        display_mode = "none"
    else:
        display_mode = "local"

    with VDevice() as target:   # Get Hailo Device and define as 'target'
        with HailoEngine(args.lane, target) as engine_lane, \
             HailoEngine(args.object, target) as engine_obj, \
             Camera(CAM_WIDTH, CAM_HEIGHT, CAM_FPS) as cam, \
             Display(DISPLAY_WIDTH, DISPLAY_HEIGHT, CAM_FPS, mode=display_mode) as display:

            last_valid_state = None
            last_route_key = None
            last_mission_state = robotaxi.state
            # vars to avoid spamming commands when not necessary
            last_sent_throttle = None
            last_sent_steering = None

            try:
                while True:
                    timer.start_loop()

                    # ── CAMERA ──────────────────────────────────────────
                    timer.start_stage("Camera")
                    rgb = cam.get_frame()
                    if rgb is None:
                        continue
                    aruco_worker.update_frame(rgb)
                    timer.end_stage("Camera")

                    # ── INFERENCE ────────────────────────────────────────
                    timer.start_stage("Inf_Lane")
                    outputs_lane = engine_lane.infer(rgb)
                    timer.end_stage("Inf_Lane")

                    timer.start_stage("Inf_Obj")
                    outputs_obj  = engine_obj.infer(rgb)
                    timer.end_stage("Inf_Obj")

                    # ── LANE POST-PROCESSING ─────────────────────────────
                    timer.start_stage("Post")
                    binary_mask = decoder.decode_to_mask(outputs_lane, CAM_HEIGHT, CAM_WIDTH)
                    clean_mask  = mask_filters.process(binary_mask)
                    bev_mask    = bev.warp(clean_mask)
                    fit_result  = fitter.fit(bev_mask)

                    # ── OBJECT DETECTION ─────────────────────────────────
                    detections = detector.process(outputs_obj, rgb.shape)
                    env_state  = build_environment_state(detections, fit_result, checker, rgb.shape)
                    rgb = detector.draw(rgb, detections)
                    timer.end_stage("Post")

                    # ── ARUCO DETECTIONS ─────────────────────────────────
                    aruco_detection = aruco_worker.get_detection()

                    aruco_id = aruco_detection.get("id")
                    aruco_distance_m = aruco_detection.get("distance_m")
                    aruco_distance_cm = aruco_detection.get("distance_cm")

                    if aruco_id is not None:
                        logging.info(
                            "ArUco detected | id=%s | distance=%.1f cm",
                            aruco_id,
                            aruco_distance_cm,
                        )

                    current_grid_pos = aruco_worker.current_grid(
                        current_grid_pos,
                        max_distance_m=0.50,
                    )

                    # ── OBSTACLE TRACKER ─────────────────────────────────
                    obs_info = obs_tracker.update(detections)

                    # ── BLIND WAIT TIMER ─────────────────────────────────
                    if fsm.state == State.BLIND_WAIT:
                        if planner.check_blind_wait_timeout():
                            fsm.signal_blind_wait_timeout()
                            planner.reset_blind_timer()
                    else:
                        planner.reset_blind_timer()

                    # ── ROBOTAXI MISSION ─────────────────────────────────
                    previous_mission_state = robotaxi.state
                    robotaxi.update(aruco_id, aruco_distance_m)

#                    taxi_maneuver = robotaxi.get_aruco_11_maneuver(
#                        aruco_id,
#                        aruco_distance_m,
#                    )
                    taxi_maneuver = robotaxi.get_taxi_maneuver(aruco_id, aruco_distance_m)
                    
                    if taxi_maneuver == TaxiManeuver.PARKING_OUT_LEFT:
                        fsm.signal_robotaxi_state(State.PARKING_OUT_LEFT, "Exiting parking zone: left bias")
                    elif taxi_maneuver == TaxiManeuver.PARKING_OUT_RIGHT:
                        fsm.signal_robotaxi_state(State.PARKING_OUT_RIGHT, "Exiting parking zone: right bias")
                    elif taxi_maneuver == TaxiManeuver.CROSS_LEFT:
                        fsm.signal_robotaxi_state(State.CROSS_LEFT, "ArUco 13: Executing cross left")
                    elif taxi_maneuver == TaxiManeuver.CROSS_RIGHT:
                        fsm.signal_robotaxi_state(State.CROSS_RIGHT, "ArUco 11 detected: leaving crossing at 50 cm")
                    elif taxi_maneuver == TaxiManeuver.PARKING_IN_LEFT:
                        fsm.signal_robotaxi_state(State.PARKING_IN_LEFT, "ArUco 11 detected: entering parking at 50 cm")
                    elif taxi_maneuver == TaxiManeuver.PARKING_IN_RIGHT:
                        fsm.signal_robotaxi_state(State.PARKING_IN_RIGHT, "ArUco 12: Approaching parking from right")

                    #aruco its not detected anymore go to retuning state (cte = 0.00)
                    elif fsm.state in TAXIROBOT_STATES and aruco_id is None:
                        fsm.state = State.RETURNING
                        planner.reset()

                    if robotaxi.state != previous_mission_state:
                        last_route_key = None

                    path = robotaxi.get_path(current_grid_pos)
                    goal = robotaxi.get_current_goal()

                    route_key = (
                        robotaxi.state,
                        current_grid_pos.row,
                        current_grid_pos.col,
                        goal.row if goal is not None else None,
                        goal.col if goal is not None else None,
                        len(path),
                    )

                    if route_key != last_route_key:
                        last_route_key = route_key

                        print_path_map(
                            path=path,
                            current_pos=current_grid_pos,
                            goal_pos=goal,
                            pickup=pickup,
                            dropoff=dropoff,
                        )

                        logging.info(
                            "Taxi state: %s | current=%s | goal=%s | path_len=%d",
                            robotaxi.state.name,
                            current_grid_pos,
                            goal,
                            len(path),
                        )

                    # ── FSM DECISION ─────────────────────────────────────
                    timer.start_stage("Decision")
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

                    # Real dt from Timer for accurate PID control
                    dt = timer.get_loop_duration() / 1000.0
                    pid_return = round(pid.update(target_cte, cte_actual, dt), 2)

                    throttle = STATE_THROTTLE.get(current_state, 0)
                    if current_state == State.FOLLOW:
                        throttle = adaptive_cruise.compute_follow_error(env_state.lead_car_area)
                    
                    # ── CAN ──────────────────────────────────────────────
                    steering = round(pid_return * -1, 2)
                    
                    if robotaxi.should_stop():
                        throttle = 0
                        steering = 0
                    
                        logging.info(
                            "ROBOTAXI STOP | state=%s | remaining=%.1fs",
                            robotaxi.state.name,
                            robotaxi.get_wait_remaining(),
                        )
                    
                    if not args.virtual:
                        if throttle != last_sent_throttle or steering != last_sent_steering:
                            can.send_drive_command(0x002, throttle, steering)
                            last_sent_throttle = throttle
                            last_sent_steering = steering

                    if last_valid_state is None or current_state.value != last_valid_state:
                        last_valid_state = current_state.value

                    timer.end_stage("Decision")

                    # ── KUKSA ────────────────────────────────────────────
                    timer.start_stage("Kuksa")
                    kuksa_channel.send(env_state.detections)
                    timer.end_stage("Kuksa")

                    # ── DISPLAY ──────────────────────────────────────────
                    timer.start_stage("Display")
                    if display_mode != "none":
                        res = draw_lane_overlay(rgb, fit_result, bev)
                        display.show(res)
                    timer.end_stage("Display")

                    timer.end_loop()
                    fps = timer.get_fps()
                    cpu_temp = hw_monitor.read_temp()
                    total_cycle_time = timer.get_loop_duration()

            except KeyboardInterrupt:
                logging.info("Shutting down...")
            finally:
                cam.stop()
                aruco_worker.stop()
                can.close()


if __name__ == "__main__":
    main()
