from dataclasses import dataclass
from enum import Enum, auto

from track_map import GridPos
from path import find_path


class TaxiState(Enum):
    DISABLED = auto()
    GOING_TO_PICKUP = auto()
    WAITING_PASSENGER = auto()
    GOING_TO_DROPOFF = auto()
    COMPLETE = auto()
    FAULT = auto()


@dataclass
class RobotaxiMission:
    car_start: GridPos
    pickup: GridPos
    dropoff: GridPos
    state: TaxiState = TaxiState.GOING_TO_PICKUP

    def get_current_goal(self) -> GridPos | None:
        if self.state == TaxiState.GOING_TO_PICKUP:
            return self.pickup

        if self.state == TaxiState.GOING_TO_DROPOFF:
            return self.dropoff

        return None

    def get_path(self, current_pos: GridPos) -> list[GridPos]:
        goal = self.get_current_goal()

        if goal is None:
            return []

        return find_path(current_pos, goal)

    def update(self, current_pos: GridPos, passenger_confirmed: bool = False) -> None:
        if self.state == TaxiState.GOING_TO_PICKUP:
            if current_pos == self.pickup:
                self.state = TaxiState.WAITING_PASSENGER

        elif self.state == TaxiState.WAITING_PASSENGER:
            if passenger_confirmed:
                self.state = TaxiState.GOING_TO_DROPOFF

        elif self.state == TaxiState.GOING_TO_DROPOFF:
            if current_pos == self.dropoff:
                self.state = TaxiState.COMPLETE