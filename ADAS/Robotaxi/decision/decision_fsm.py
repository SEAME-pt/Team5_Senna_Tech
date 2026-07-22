import logging
import time
from enum import Enum
from collections import deque
from object.perception_objects import EnvironmentState, ClassID

log = logging.getLogger("FSM")

class State(Enum):
    STOP         = 0
    SPEED_SLOW   = 5
    SPEED_50     = 9
    SPEED_80     = 11
    FOLLOW       = 4
    RETURNING    = 14

    PARKING_OUT_LEFT    = 30
    PARKING_OUT_RIGHT   = 31
    CROSS_LEFT          = 32
    CROSS_RIGHT         = 33
    PARKING_IN_LEFT     = 34
    PARKING_IN_RIGHT    = 35

TAXIROBOT_STATES = (
    State.PARKING_OUT_LEFT,
    State.PARKING_OUT_RIGHT,
    State.CROSS_LEFT,
    State.CROSS_RIGHT,
    State.PARKING_IN_LEFT,
    State.PARKING_IN_RIGHT,
)

STATE_THROTTLE = {
    State.STOP:          0,
    State.SPEED_SLOW:    5,
    State.SPEED_50:      9,
    State.SPEED_80:      11,
    State.FOLLOW:        0,
    State.RETURNING:     5,
    State.PARKING_OUT_LEFT:  4,
    State.PARKING_OUT_RIGHT: 4,
    State.CROSS_LEFT:        5,
    State.CROSS_RIGHT:       5,
    State.PARKING_IN_LEFT:   5,
    State.PARKING_IN_RIGHT:  5,
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

        self._buf_stop_red     = ConfirmationBuffer(2)
        self._buf_stop_sign    = ConfirmationBuffer(2)
        self._buf_slow         = ConfirmationBuffer(2)
        self._buf_speed_50     = ConfirmationBuffer(2)
        self._buf_speed_80     = ConfirmationBuffer(2)
        self._buf_follow       = ConfirmationBuffer(5)
        self._buf_follow_exit  = ConfirmationBuffer(15)

    def process(
        self,
        env: EnvironmentState,
        planner_return_complete: bool = False,
    ) -> State:

        cond = self._evaluate_environment(env)

        if self.state == State.RETURNING:
            if planner_return_complete:
                self._transition(State.SPEED_50, "Corridor clear")
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

    def _evaluate_environment(self, env: EnvironmentState) -> dict:
        cond = {
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

            if d.in_corridor and d.class_id == ClassID.CAR:
                if self.state != State.FOLLOW and d.relative_area >= Thresholds.AREA_FOLLOW_ENTER:
                    cond["follow"] = True
                elif self.state == State.FOLLOW and d.relative_area >= Thresholds.AREA_FOLLOW_EXIT:
                    cond["follow"] = True

        return cond

    """
    Change to a Robotaxi maneuver state.
    Emergency, avoidance and stop situations keep priority.
    """
    def signal_robotaxi_state(self, new_state: State, reason: str) -> bool:

        if new_state not in TAXIROBOT_STATES:
            return False

        if self.state == State.STOP:
            return False

        self._transition(new_state, reason)
        return True


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
        self._buf_follow_exit.reset()
