from dataclasses import dataclass
from enum import Enum, auto

from map.track_map import GridPos
from map.path import find_path


class TaxiState(Enum):
    DISABLED = auto()
    GOING_TO_PICKUP = auto()
    GOING_TO_DROPOFF = auto()
    COMPLETE = auto()
    FAULT = auto()


@dataclass
class RobotaxiMission:
    car_start: GridPos
    pickup: GridPos
    dropoff: GridPos
    pickup_aruco_id: int
    dropoff_aruco_id: int
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

    # Advance the mission state based on the detected ArUco marker.
    def update(self, detected_aruco_id: int | None) -> None:
        if self.state == TaxiState.GOING_TO_PICKUP:
            # Pickup marker detected, continue to dropoff automatically.
            if detected_aruco_id == self.pickup_aruco_id:
                self.state = TaxiState.GOING_TO_DROPOFF

        elif self.state == TaxiState.GOING_TO_DROPOFF:
            # Dropoff marker detected, mission is complete.
            if detected_aruco_id == self.dropoff_aruco_id:
                self.state = TaxiState.COMPLETE
