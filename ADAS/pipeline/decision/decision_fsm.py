import logging
from enum import Enum, auto
from collections import deque
from dataclasses import dataclass
from ..object.perception_objects import EnvironmentState, ClassID

log = logging.getLogger("FSM")

class State(Enum):
    FREE = 0
    FOLLOW = 1
    SLOW = 2
    STOP = 3
    EMERGENCY = 4

@dataclass
class MotorIntent:
    target_speed_pct: float  # -1.0 (100% Reverse) a 1.0 (100% Forward)
    estop_trigger: bool = False

class ConfirmationBuffer:
    def __init__(self, size: int):
        self._buf = deque(maxlen=size)
        self._size = size
    def update(self, condition: bool) -> bool:
        if condition: self._buf.append(condition)
        else: self.reset()
        return len(self._buf) == self._size and all(self._buf)
    def reset(self): self._buf.clear()

class Thresholds:
    AREA_EMERGENCY = 0.20
    AREA_SLOW      = 0.08
    AREA_FOLLOW    = 0.02
    
    SPEED_FREE   = 0.80  # 80% Throttle
    SPEED_FOLLOW = 0.40  # 40% Throttle
    SPEED_SLOW   = 0.25  # 25% Throttle
    SPEED_STOP   = 0.00  # Coast/Brake

class VehicleFSM:
    def __init__(self):
        self.state = State.FREE
        self._buf_emergency = ConfirmationBuffer(2)
        self._buf_stop      = ConfirmationBuffer(5)
        self._buf_slow      = ConfirmationBuffer(4)
        self._buf_clear     = ConfirmationBuffer(15)

    def process(self, env: EnvironmentState) -> tuple[State, MotorIntent]:
        """A FSM avalia o estado do mundo e devolve (NovoEstado, IntençõesDeMotor)"""
        cond = self._evaluate_environment(env)
        
        # ── EMERGENCY (Latching) ──
        if self.state == State.EMERGENCY:
            if self._buf_clear.update(env.corridor_clear):
                self._transition(State.FREE, "Corridor finally clear")
            else:
                return self.state, MotorIntent(target_speed_pct=0.0, estop_trigger=True)

        # ── Transições Normais ──
        if self._buf_emergency.update(cond["emergency"]):
            self._transition(State.EMERGENCY, "Critical Obstacle!")
            self._reset_buffers()
            return self.state, MotorIntent(target_speed_pct=0.0, estop_trigger=True)

        elif self._buf_stop.update(cond["stop"]):
            self._transition(State.STOP, "Red Light / Stop Sign")
        elif self._buf_slow.update(cond["slow"]):
            self._transition(State.SLOW, "Hazard / Crosswalk ahead")
        elif self._buf_clear.update(env.corridor_clear):
            self._transition(State.FREE, "Path Clear")

        return self.state, self._get_motor_intent()

    def _evaluate_environment(self, env: EnvironmentState) -> dict:
        cond = {"emergency": False, "stop": False, "slow": False, "follow": False}
        
        for d in env.detections:
            if not d.in_corridor: continue
            
            if d.class_id in (ClassID.CAR, ClassID.OBSTACLE) and d.relative_area >= Thresholds.AREA_EMERGENCY:
                cond["emergency"] = True
            elif d.class_id in (ClassID.TRAFFIC_LIGHT_RED, ClassID.STOP_SIGN, ClassID.GATE):
                cond["stop"] = True
            elif d.class_id in (ClassID.TRAFFIC_LIGHT_YELLOW, ClassID.CROSSWALK_SIGN):
                cond["slow"] = True
                
        # Injectar a lógica da distância da passadeira (Vinda das Linhas!)
        if env.crosswalk_distance_m is not None:
            if env.crosswalk_distance_m < 3.0:
                cond["stop"] = True  # Perto demais, parar.
            elif env.crosswalk_distance_m < 10.0:
                cond["slow"] = True  # Reduzir velocidade.
                
        return cond

    def _get_motor_intent(self) -> MotorIntent:
        speed_map = {
            State.FREE: Thresholds.SPEED_FREE,
            State.FOLLOW: Thresholds.SPEED_FOLLOW,
            State.SLOW: Thresholds.SPEED_SLOW,
            State.STOP: Thresholds.SPEED_STOP,
            State.EMERGENCY: 0.0
        }
        return MotorIntent(target_speed_pct=speed_map[self.state])

    def _transition(self, new_state: State, reason: str):
        if self.state != new_state:
            log.info(f"FSM Transition: {self.state.name} -> {new_state.name} [{reason}]")
            self.state = new_state

    def _reset_buffers(self):
        self._buf_stop.reset()
        self._buf_slow.reset()