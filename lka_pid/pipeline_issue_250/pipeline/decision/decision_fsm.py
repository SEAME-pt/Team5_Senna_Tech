import logging
from enum import Enum
from collections import deque
from object.perception_objects import EnvironmentState, ClassID

# Logger para debug de transições
log = logging.getLogger("FSM")

# Os estados vão ser enviados diretamente pelo seu valor (0, 1, 2, 3, 4, 5) para o CAN
class State(Enum):
    FREE = 0
    EMERGENCY = 1
    RESET = 2
    FOLLOW = 3
    SLOW = 4
    STOP = 5
    SPEED_50 = 6
    SPEED_80 = 7

class ConfirmationBuffer:
    def __init__(self, size: int):
        self._buf = deque(maxlen=size)
        self._size = size
        
    def update(self, condition: bool) -> bool:
        if condition: self._buf.append(condition)
        else: self.reset()
        return len(self._buf) == self._size and all(self._buf)
        
    def reset(self): 
        self._buf.clear()

class Thresholds:
    # Apenas os limiares de perceção espacial se mantêm
    AREA_EMERGENCY = 0.20
    AREA_SLOW      = 0.08
    AREA_FOLLOW    = 0.02

class VehicleFSM:
    def __init__(self):
        self.state = State.FREE
        #em ( ) é a quantidade de frames consecutivos necessários para confirmar a transição de estado
        self._buf_emergency = ConfirmationBuffer(4)
        self._buf_stop      = ConfirmationBuffer(7)
        self._buf_slow      = ConfirmationBuffer(6)
        self._buf_speed_50  = ConfirmationBuffer(6)
        self._buf_speed_80  = ConfirmationBuffer(6)
        self._buf_clear     = ConfirmationBuffer(15)

    def process(self, env: EnvironmentState) -> State:
        """A FSM avalia o estado do mundo e devolve o Estado enumerado atual."""
        cond = self._evaluate_environment(env)
        
        # ── EMERGENCY (Latching) ──
        if self.state == State.EMERGENCY:
            if self._buf_clear.update(env.corridor_clear):
                self._transition(State.FREE, "Corridor finally clear")
            return self.state

        # ── Transições Normais ──
        if self._buf_emergency.update(cond["emergency"]):
            self._transition(State.EMERGENCY, "Critical Obstacle!")
            self._reset_buffers()
            return self.state

        elif self._buf_stop.update(cond["stop"]):
            self._transition(State.STOP, "Red Light / Stop Sign")
        elif self._buf_slow.update(cond["slow"]):
            self._transition(State.SLOW, "Hazard / Crosswalk ahead")
        elif self._buf_speed_50.update(cond["speed_50"]):
            self._transition(State.SPEED_50, "Speed Limit 50 detected")    
        elif self._buf_speed_80.update(cond["speed_80"]):
            self._transition(State.SPEED_80, "Speed Limit 80 detected")
        elif self._buf_clear.update(env.corridor_clear):
            self._transition(State.FREE, "Path Clear")

        return self.state

    def _evaluate_environment(self, env: EnvironmentState) -> dict:
        cond = {
            "emergency": False, 
            "stop": False, 
            "slow": False, 
            "follow": False,
            "speed_50": False,
            "speed_80": False
        }
        
        for d in env.detections:
            # Sinais afetam o carro independentemente de estarem na faixa
            if d.class_id in (ClassID.LIGHT_RED, ClassID.STOP_SIGN, ClassID.GATE):
                cond["stop"] = True
            elif d.class_id in (ClassID.LIGHT_YELLOW, ClassID.CROSSWALK_SIGN):
                cond["slow"] = True
            elif d.class_id == ClassID.SIGN_50:
                cond["speed_50"] = True
            elif d.class_id == ClassID.SIGN_80:
                cond["speed_80"] = True
                
            # Obstáculos SÓ importam se estiverem NO CORREDOR
            if d.in_corridor and d.class_id in (ClassID.CAR, ClassID.OBSTACLE):
                if d.relative_area >= Thresholds.AREA_EMERGENCY:
                    cond["emergency"] = True
                
        # Lógica geométrica de passadeiras
        if env.crosswalk_distance_m is not None:
            if env.crosswalk_distance_m < 3.0:
                cond["stop"] = True
            elif env.crosswalk_distance_m < 10.0:
                cond["slow"] = True
                
        return cond

    def _transition(self, new_state: State, reason: str):
        if self.state != new_state:
            log.info(f"FSM Transition: {self.state.name} -> {new_state.name} [{reason}]")
            self.state = new_state

    def _reset_buffers(self):
        self._buf_stop.reset()
        self._buf_slow.reset()
        self._buf_speed_50.reset()
        self._buf_speed_80.reset()