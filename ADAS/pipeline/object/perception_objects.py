from enum import IntEnum, Enum
from dataclasses import dataclass
from typing import List, Optional


class ClassID(IntEnum):
    SIGN_50 = 0
    SIGN_80 = 1
    GATE = 2
    CROSSWALK_SIGN = 3
    STOP_SIGN = 4
    YIELD_SIGN = 5
    CAR = 6
    DANGER_SIGN = 7
    OBSTACLE = 8
    LIGHT_GREEN = 9
    LIGHT_OFF = 10
    LIGHT_RED = 11
    LIGHT_YELLOW = 12


class ObstacleSituation(Enum):
    CLEAR     = "clear"
    AVOIDANCE = "avoidance"
    BRAKE     = "brake"


@dataclass
class Detection:
    class_id: ClassID
    in_corridor: bool
    relative_area: float


@dataclass
class EnvironmentState:
    detections: List[Detection]
    corridor_clear: bool
    lead_car_detected: bool = False
    lead_car_area: float = 0.0
