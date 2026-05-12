import logging
import time
from enum import Enum
from collections import deque
from object.perception_objects import EnvironmentState, ClassID

# Logger para debug de transições
log = logging.getLogger("FSM")


# Os estados vão ser enviados diretamente pelo valor para o CAN
class State(Enum):
    EMERGENCY = 0
    STOP = 1
    SPEED_SLOW = 2
    SPEED_50 = 3
    SPEED_80 = 4
    FOLLOW = 5


class StopReason(Enum):
    NONE = 0
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

        return (
            len(self._buf) == self._size
            and all(self._buf)
        )

    def reset(self):
        self._buf.clear()


class Thresholds:
    AREA_EMERGENCY = 0.05
    AREA_SIGN = 0.004
    AREA_TRAFFIC_LIGHT = 0.004
    AREA_CAR = 0.004


class VehicleFSM:
    def __init__(self):
        self.state = State.SPEED_50

        # motivo do STOP
        self.stop_reason = StopReason.NONE

        # timestamp usado para STOP_SIGN
        self.stop_timestamp = None
        self.stop_sign_ignore_until = 0
        self.STOP_SIGN_COOLDOWN = 5

        # buffers de confirmação
        self._buf_emergency = ConfirmationBuffer(1)
        self._buf_stop_red = ConfirmationBuffer(2)
        self._buf_stop_sign = ConfirmationBuffer(2)
        self._buf_slow = ConfirmationBuffer(2)
        self._buf_speed_50 = ConfirmationBuffer(2)
        self._buf_speed_80 = ConfirmationBuffer(2)
        self._buf_clear = ConfirmationBuffer(15)

    def process(self, env: EnvironmentState) -> State:

        cond = self._evaluate_environment(env)

        # ─────────────────────────────
        # EMERGENCY (latching)
        # ─────────────────────────────
        if self.state == State.EMERGENCY:

            if self._buf_clear.update(env.corridor_clear):
                self._transition(
                    State.SPEED_50,
                    "Corridor clear"
                )

                self._reset_buffers()

            return self.state

        # ─────────────────────────────
        # STOP logic
        # ─────────────────────────────
        if self.state == State.STOP:

            # STOP causado por semáforo vermelho
            if self.stop_reason == StopReason.RED_LIGHT:

                if cond["green_light"]:
                    self._transition(
                        State.SPEED_50,
                        "Green light detected"
                    )

                    self.stop_reason = StopReason.NONE
                    self.stop_timestamp = None

                    self._reset_buffers()

                return self.state

            # STOP causado por placa STOP
            elif self.stop_reason == StopReason.STOP_SIGN:

                if (
                    self.stop_timestamp is not None
                    and time.time() - self.stop_timestamp >= 5
                ):
                    self._transition(
                        State.SPEED_50,
                        "5 seconds completed"
                    )

                    self.stop_reason = StopReason.NONE
                    self.stop_timestamp = None

                    # ignora novas STOP_SIGN por 5s
                    self.stop_sign_ignore_until = (
                        time.time() + self.STOP_SIGN_COOLDOWN
                    )

                    self._reset_buffers()

                return self.state

        # ─────────────────────────────
        # NORMAL transitions
        # ─────────────────────────────

        # EMERGENCY
        if self._buf_emergency.update(cond["emergency"]):

            self._transition(
                State.EMERGENCY,
                "Critical obstacle"
            )

            self._reset_buffers()

            return self.state

        # RED LIGHT
        elif self._buf_stop_red.update(cond["stop_red"]):

            self._transition(
                State.STOP,
                "Red light"
            )

            self.stop_reason = StopReason.RED_LIGHT
            self.stop_timestamp = None

            self._reset_buffers()

        # STOP SIGN
        elif (
            time.time() >= self.stop_sign_ignore_until
            and self._buf_stop_sign.update(cond["stop_sign"])
        ):

            self._transition(
                State.STOP,
                "Stop sign"
            )

            self.stop_reason = StopReason.STOP_SIGN
            self.stop_timestamp = time.time()

            self._reset_buffers()

        # SLOW
        elif self._buf_slow.update(cond["slow"]):

            self._transition(
                State.SPEED_SLOW,
                "Slow zone"
            )

        # SPEED 50
        elif self._buf_speed_50.update(cond["speed_50"]):

            self._transition(
                State.SPEED_50,
                "Speed 50"
            )

        # SPEED 80
        elif self._buf_speed_80.update(cond["speed_80"]):

            self._transition(
                State.SPEED_80,
                "Speed 80"
            )

        elif cond["follow"]:
            self._transition(
                State.FOLLOW,
                "Following lead car"
            )

        return self.state

    def _evaluate_environment(
        self,
        env: EnvironmentState
    ) -> dict:

        cond = {
            "emergency": False,
            "stop_red": False,
            "stop_sign": False,
            "green_light": False,
            "slow": False,
            "follow": False,
            "speed_50": False,
            "speed_80": False
        }

        for d in env.detections:

            # ─────────────────────────
            # Traffic lights / signs
            # ─────────────────────────

            print(
                f"[DEBUG] class={d.class_id.name} "
                f"(id={d.class_id.value}) | "
                f"area={d.relative_area:.4f}"
            )
            
            if d.class_id == ClassID.LIGHT_RED and d.relative_area > Thresholds.AREA_TRAFFIC_LIGHT:
                cond["stop_red"] = True

            elif d.class_id == ClassID.STOP_SIGN and d.relative_area > Thresholds.AREA_SIGN:
                cond["stop_sign"] = True

            elif d.class_id == ClassID.LIGHT_GREEN and d.relative_area > Thresholds.AREA_TRAFFIC_LIGHT:
                cond["green_light"] = True

            elif d.class_id in (
                ClassID.LIGHT_YELLOW,
                ClassID.CROSSWALK_SIGN
            ):
                cond["slow"] = True

            elif d.class_id == ClassID.SIGN_50 and d.relative_area > Thresholds.AREA_SIGN:
                cond["speed_50"] = True

            elif d.class_id == ClassID.SIGN_80 and d.relative_area > Thresholds.AREA_SIGN:
                cond["speed_80"] = True

            # ─────────────────────────
            # Obstáculos no corredor
            # ─────────────────────────

            if (d.in_corridor):
                if (d.relative_area >= Thresholds.AREA_EMERGENCY and d.class_id == ClassID.OBSTACLE):
                    cond["emergency"] = True
                if (d.relative_area >= Thresholds.AREA_FOLLOW):
                    cond["follow"] = True
        # ─────────────────────────────
        # Crosswalk geometry
        # ─────────────────────────────

        if env.crosswalk_distance_m is not None:

            if env.crosswalk_distance_m < 3.0:
                cond["stop_sign"] = True

            elif env.crosswalk_distance_m < 10.0:
                cond["slow"] = True

        return cond

    def _transition(
        self,
        new_state: State,
        reason: str
    ):

        if self.state != new_state:

            log.info(
                f"FSM Transition: "
                f"{self.state.name} -> "
                f"{new_state.name} "
                f"[{reason}]"
            )

            self.state = new_state

    def _reset_buffers(self):

        self._buf_stop_red.reset()
        self._buf_stop_sign.reset()
        self._buf_slow.reset()
        self._buf_speed_50.reset()
        self._buf_speed_80.reset()