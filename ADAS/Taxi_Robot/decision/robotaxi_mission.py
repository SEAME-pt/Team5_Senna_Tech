from dataclasses import dataclass
from enum import Enum, auto
import time

from map.track_map import GridPos
from map.path import find_path


class TaxiState(Enum):
    DISABLED = auto()
    GOING_TO_PICKUP = auto()
    WAITING_AT_PICKUP = auto()
    GOING_TO_DROPOFF = auto()
    WAITING_AT_DROPOFF = auto()
    RETURNING_TO_PARKING = auto()
    COMPLETE = auto()
    FAULT = auto()


@dataclass
class RobotaxiMission:
    parking: GridPos
    pickup: GridPos
    dropoff: GridPos
    parking_aruco_id: int
    pickup_aruco_id: int
    dropoff_aruco_id: int
    state: TaxiState = TaxiState.GOING_TO_PICKUP
    stop_distance_m: float = 0.40
    stop_duration_s: float = 5.0
    stop_started_at: float | None = None

    def get_current_goal(self) -> GridPos | None:
        if self.state in (
            TaxiState.GOING_TO_PICKUP,
            TaxiState.WAITING_AT_PICKUP,
        ):
            return self.pickup

        if self.state in (
            TaxiState.GOING_TO_DROPOFF,
            TaxiState.WAITING_AT_DROPOFF,
        ):
            return self.dropoff

        if self.state == TaxiState.RETURNING_TO_PARKING:
            return self.parking

        return None

    def get_path(self, current_pos: GridPos) -> list[GridPos]:
        goal = self.get_current_goal()

        if goal is None:
            return []

        return find_path(current_pos, goal)

    def update(
        self,
        detected_aruco_id: int | None,
        detected_distance_m: float | None,
    ) -> None:
        now = time.monotonic()

        if self.state == TaxiState.GOING_TO_PICKUP:
            if self._target_reached(
                detected_aruco_id,
                detected_distance_m,
                self.pickup_aruco_id,
            ):
                self.state = TaxiState.WAITING_AT_PICKUP
                self.stop_started_at = now
                print("Pickup reached. Stopping for 5 seconds.")

        elif self.state == TaxiState.WAITING_AT_PICKUP:
            if self._stop_finished(now):
                self.state = TaxiState.GOING_TO_DROPOFF
                self.stop_started_at = None
                print("Pickup stop complete. Going to dropoff.")

        elif self.state == TaxiState.GOING_TO_DROPOFF:
            if self._target_reached(
                detected_aruco_id,
                detected_distance_m,
                self.dropoff_aruco_id,
            ):
                self.state = TaxiState.WAITING_AT_DROPOFF
                self.stop_started_at = now
                print("Dropoff reached. Stopping for 5 seconds.")

        elif self.state == TaxiState.WAITING_AT_DROPOFF:
            if self._stop_finished(now):
                self.state = TaxiState.RETURNING_TO_PARKING
                self.stop_started_at = None
                print("Dropoff stop complete. Returning to parking.")

        elif self.state == TaxiState.RETURNING_TO_PARKING:
            if self._target_reached(
                detected_aruco_id,
                detected_distance_m,
                self.parking_aruco_id,
            ):
                self.state = TaxiState.COMPLETE
                print("Parking reached. Robotaxi mission complete.")

    def _target_reached(
        self,
        detected_aruco_id: int | None,
        detected_distance_m: float | None,
        target_aruco_id: int,
    ) -> bool:
        if detected_aruco_id is None or detected_distance_m is None:
            return False

        return (
            detected_aruco_id == target_aruco_id
            and detected_distance_m <= self.stop_distance_m
        )

    def _stop_finished(self, now: float) -> bool:
        if self.stop_started_at is None:
            return False

        return now - self.stop_started_at >= self.stop_duration_s

    def should_stop(self) -> bool:
        return self.state in (
            TaxiState.WAITING_AT_PICKUP,
            TaxiState.WAITING_AT_DROPOFF,
            TaxiState.COMPLETE,
        )

    def get_wait_remaining(self) -> float:
        if self.stop_started_at is None:
            return 0.0

        remaining = self.stop_duration_s - (
            time.monotonic() - self.stop_started_at
        )

        if remaining < 0.0:
            return 0.0

        return remaining