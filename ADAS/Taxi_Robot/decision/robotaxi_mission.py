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

    # Return the route from the current position to the mission goal.
    def get_path(self, current_pos: GridPos) -> list[GridPos]:
        goal = self.get_current_goal()

        if goal is None:
            return []

        return find_path(current_pos, goal)

    # Advance the mission state based on current position and passenger status.
    def update(self, current_pos: GridPos, passenger_confirmed: bool = False) -> None:
        if self.state == TaxiState.GOING_TO_PICKUP:
            # Reached pickup point, now wait for passenger boarding confirmation.
            if current_pos == self.pickup:
                self.state = TaxiState.WAITING_PASSENGER

        elif self.state == TaxiState.WAITING_PASSENGER:
            # Passenger confirmed, continue to the dropoff point.
            if passenger_confirmed:
                self.state = TaxiState.GOING_TO_DROPOFF

        elif self.state == TaxiState.GOING_TO_DROPOFF:
            # Reached dropoff point, mission is complete.
            if current_pos == self.dropoff:
                self.state = TaxiState.COMPLETE
