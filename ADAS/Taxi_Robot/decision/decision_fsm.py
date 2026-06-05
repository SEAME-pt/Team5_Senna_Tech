import logging
import time
from enum import Enum
from collections import deque
from object.perception_objects import EnvironmentState, ClassID, ObstacleSituation

log = logging.getLogger("FSM")

class State(Enum):
    EMERGENCY    = 200
    STOP         = 0
    SPEED_SLOW   = 5
    SPEED_50     = 8
    SPEED_80     = 10
    FOLLOW       = 4
    PREPARE_AVOID = 11
    AVOIDING     = 12
    BLIND_WAIT   = 13
    RETURNING    = 14

AVOIDANCE_STATES = (
    State.PREPARE_AVOID,
    State.AVOIDING,
    State.BLIND_WAIT,
    State.RETURNING,
)

STATE_THROTTLE = {
    State.EMERGENCY:     200,
    State.STOP:          0,
    State.SPEED_SLOW:    5,
    State.SPEED_50:      8,
    State.SPEED_80:      10,
    State.FOLLOW:        0,
    State.PREPARE_AVOID: 5,
    State.AVOIDING:      5,
    State.BLIND_WAIT:    5,
    State.RETURNING:     5,
}

class StopReason(Enum):
    NONE      = 0
    RED_LIGHT = 1
    STOP_SIGN = 2

class ConfirmationBuffer:
    def __init__(self, size: int):
        self._buf = deque(maxlen=size)
        self._size = size

    def update(self, condition: bool) -> bool:
        if condition:
            self._buf.append(True)
        else:
            self.reset()
        return len(self._buf) == self._size and all(self._buf)

    def reset(self):
        self._buf.clear()


class Thresholds:
    AREA_EMERGENCY      = 0.05
    AREA_AVOIDANCE      = 0.015
    AREA_SIGN           = 0.006
    AREA_TRAFFIC_LIGHT  = 0.006
    AREA_CAR            = 0.004
    AREA_FOLLOW_ENTER   = 0.022
    AREA_FOLLOW_EXIT    = 0.017


class VehicleFSM:
    def __init__(self):
        self.state      = State.SPEED_50
        self.stop_reason = StopReason.NONE

        self.stop_timestamp        = None
        self.stop_sign_ignore_until = 0
        self.STOP_SIGN_COOLDOWN    = 5

        self._buf_emergency    = ConfirmationBuffer(3)
        self._buf_stop_red     = ConfirmationBuffer(2)
        self._buf_stop_sign    = ConfirmationBuffer(2)
        self._buf_slow         = ConfirmationBuffer(2)
        self._buf_speed_50     = ConfirmationBuffer(2)
        self._buf_speed_80     = ConfirmationBuffer(2)
        self._buf_clear        = ConfirmationBuffer(8)
        self._buf_avoid        = ConfirmationBuffer(5)
        self._buf_follow       = ConfirmationBuffer(5)
        self._buf_follow_exit  = ConfirmationBuffer(15)

        self._prepare_buf             = ConfirmationBuffer(2)
        self.frames_without_obstacle  = 0
        self.OBSTACLE_LOST_THRESHOLD  = 10
        self._pre_avoidance_state     = State.SPEED_50

    def process(
        self,
        env: EnvironmentState,
        obstacle_situation: ObstacleSituation,
        planner_return_complete: bool = False,
    ) -> State:

        cond = self._evaluate_environment(env)

        if obstacle_situation == ObstacleSituation.BRAKE:
            self._transition(State.EMERGENCY, "Sudden brake detected by tracker")
            self._reset_buffers()
            return self.state

        if self.state in AVOIDANCE_STATES:
            return self._handle_avoidance_sequence(env, obstacle_situation, planner_return_complete)

        if self.state == State.EMERGENCY:
            if self._buf_clear.update(env.corridor_clear):
                self._transition(State.SPEED_50, "Corridor clear")
                self._reset_buffers()
            return self.state

        if self._buf_emergency.update(cond["emergency"]):
            self._transition(State.EMERGENCY, "Critical obstacle")
            self._reset_buffers()
            return self.state

        avoidance_detected = (
            obstacle_situation == ObstacleSituation.AVOIDANCE
            or cond["obstacle_ahead"]
        )

        if self._buf_avoid.update(avoidance_detected):
            if self.state in (State.SPEED_50, State.SPEED_80, State.SPEED_SLOW):
                self._pre_avoidance_state = self.state
            self._transition(State.PREPARE_AVOID, "Obstacle detected ahead")
            self._reset_buffers()
            return self.state

        if self.state == State.FOLLOW:
            if not cond["follow"]:
                if self._buf_follow_exit.update(True):
                    self._transition(State.SPEED_50, "Lead car gone")
                    self._buf_follow_exit.reset()
            else:
                self._buf_follow_exit.reset()
            return self.state

        if self.state == State.STOP:
            if self.stop_reason == StopReason.RED_LIGHT:
                if cond["green_light"]:
                    self._transition(State.SPEED_50, "Green light detected")
                    self.stop_reason   = StopReason.NONE
                    self.stop_timestamp = None
                    self._reset_buffers()
                return self.state

            elif self.stop_reason == StopReason.STOP_SIGN:
                if self.stop_timestamp is not None and time.time() - self.stop_timestamp >= 5:
                    self._transition(State.SPEED_50, "5 seconds completed")
                    self.stop_reason            = StopReason.NONE
                    self.stop_timestamp         = None
                    self.stop_sign_ignore_until = time.time() + self.STOP_SIGN_COOLDOWN
                    self._reset_buffers()
                return self.state

            else:
                return self.state

        if self._buf_stop_red.update(cond["stop_red"]):
            self._transition(State.STOP, "Red light")
            self.stop_reason    = StopReason.RED_LIGHT
            self.stop_timestamp = None
            self._reset_buffers()

        elif time.time() >= self.stop_sign_ignore_until and self._buf_stop_sign.update(cond["stop_sign"]):
            self._transition(State.STOP, "Stop sign")
            self.stop_reason    = StopReason.STOP_SIGN
            self.stop_timestamp = time.time()
            self._reset_buffers()

        elif self._buf_slow.update(cond["slow"]):
            self._transition(State.SPEED_SLOW, "Slow zone")

        elif self._buf_speed_50.update(cond["speed_50"]):
            self._transition(State.SPEED_50, "Speed 50")

        elif self._buf_speed_80.update(cond["speed_80"]):
            self._transition(State.SPEED_80, "Speed 80")

        elif self._buf_follow.update(cond["follow"]):
            self._transition(State.FOLLOW, "Following vehicle")

        return self.state

    def _handle_avoidance_sequence(
        self,
        env,
        obstacle_situation,
        planner_return_complete: bool,
    ) -> State:
        if self.state == State.PREPARE_AVOID:
            if self._prepare_buf.update(True):
                self._transition(State.AVOIDING, "Beginning of evasive maneuver")
                self.frames_without_obstacle = 0
                self._prepare_buf.reset()

        elif self.state == State.AVOIDING:
            obstacle_visible = any(
                d.class_id == ClassID.OBSTACLE and d.in_corridor
                for d in env.detections
            )
            if obstacle_visible:
                self.frames_without_obstacle = 0
            else:
                self.frames_without_obstacle += 1

            if self.frames_without_obstacle >= self.OBSTACLE_LOST_THRESHOLD:
                self._transition(State.BLIND_WAIT, "Obstacle lost, entering blind wait")
                self.frames_without_obstacle = 0

        elif self.state == State.BLIND_WAIT:
            pass

        elif self.state == State.RETURNING:
            if planner_return_complete:
                self._transition(
                    self._pre_avoidance_state,
                    f"Maneuver completed, restoring {self._pre_avoidance_state.name}"
                )
                self.frames_without_obstacle = 0
                self._reset_buffers()

        return self.state

    def signal_blind_wait_timeout(self):
        if self.state == State.BLIND_WAIT:
            self._transition(State.RETURNING, "Time to return after blind wait")

    def _evaluate_environment(self, env: EnvironmentState) -> dict:
        cond = {
            "emergency":     False,
            "obstacle_ahead": False,
            "stop_red":      False,
            "stop_sign":     False,
            "green_light":   False,
            "slow":          False,
            "follow":        False,
            "speed_50":      False,
            "speed_80":      False,
        }

        for d in env.detections:
            if d.class_id == ClassID.LIGHT_RED and d.relative_area > Thresholds.AREA_TRAFFIC_LIGHT:
                cond["stop_red"] = True
            elif d.class_id == ClassID.STOP_SIGN and d.relative_area > Thresholds.AREA_SIGN:
                cond["stop_sign"] = True
            elif d.class_id == ClassID.LIGHT_GREEN and d.relative_area > Thresholds.AREA_TRAFFIC_LIGHT:
                cond["green_light"] = True
            elif d.class_id == ClassID.CROSSWALK_SIGN and d.relative_area > Thresholds.AREA_SIGN:
                cond["slow"] = True
            elif d.class_id == ClassID.LIGHT_YELLOW and d.relative_area > Thresholds.AREA_TRAFFIC_LIGHT:
                cond["slow"] = True
            elif d.class_id == ClassID.SIGN_50 and d.relative_area > Thresholds.AREA_SIGN:
                cond["speed_50"] = True
            elif d.class_id == ClassID.SIGN_80 and d.relative_area > Thresholds.AREA_SIGN:
                cond["speed_80"] = True

            if d.in_corridor and d.class_id == ClassID.OBSTACLE:
                if d.relative_area >= Thresholds.AREA_EMERGENCY:
                    cond["emergency"] = True
                if d.relative_area >= Thresholds.AREA_AVOIDANCE:
                    cond["obstacle_ahead"] = True

            if d.in_corridor and d.class_id == ClassID.CAR:
                if self.state != State.FOLLOW and d.relative_area >= Thresholds.AREA_FOLLOW_ENTER:
                    cond["follow"] = True
                elif self.state == State.FOLLOW and d.relative_area >= Thresholds.AREA_FOLLOW_EXIT:
                    cond["follow"] = True

        return cond

    def _transition(self, new_state: State, reason: str):
        if self.state != new_state:
            log.info("FSM Transition: %s -> %s [%s]", self.state.name, new_state.name, reason)
            self.state = new_state

    def _reset_buffers(self):
        self._buf_stop_red.reset()
        self._buf_stop_sign.reset()
        self._buf_slow.reset()
        self._buf_speed_50.reset()
        self._buf_speed_80.reset()
        self._buf_avoid.reset()
        self._buf_follow_exit.reset()
