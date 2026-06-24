from dataclasses import dataclass
from enum import Enum, auto
import time

from map.track_map import GridPos
from map.path import find_path

# High-level mission states for the Robo Taxi.
#
# The normal mission flow is:
#
# GOING_TO_PICKUP
# -> WAITING_AT_PICKUP
# -> GOING_TO_DROPOFF
# -> WAITING_AT_DROPOFF
# -> RETURNING_TO_PARKING
# -> COMPLETE

class TaxiState(Enum):
    DISABLED = auto()
    GOING_TO_PICKUP = auto()
    WAITING_AT_PICKUP = auto()
    GOING_TO_DROPOFF = auto()
    WAITING_AT_DROPOFF = auto()
    RETURNING_TO_PARKING = auto()
    COMPLETE = auto()
    FAULT = auto()


class TaxiManeuver(Enum):
    NONE = auto()
    ENTER_STREET_LEFT = auto()
    ENTER_PARKING_LEFT = auto()


@dataclass
class RobotaxiMission:
    # Fixed parking position where the car starts and finishes.
    parking: GridPos

    # Passenger pickup and final dropoff positions.
    pickup: GridPos
    dropoff: GridPos

    # ArUco IDs associated with the relevant mission positions.
    parking_aruco_id: int
    pickup_aruco_id: int
    dropoff_aruco_id: int

    state: TaxiState = TaxiState.GOING_TO_PICKUP

    # Distance from a target ArUco marker at which the car
    # considers that it has reached the target and should stop.
    stop_distance_m: float = 0.45

    stop_duration_s: float = 5.0
    stop_started_at: float | None = None

    # ArUco 11 thresholds.
    exit_parking_distance_m: float = 0.70
    outside_decision_distance_m: float = 0.50

    # True only at the start of the mission.
    parking_exit_pending: bool = True

    # Prevents repeating the same action every frame.
    aruco_11_armed: bool = True

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

    """
    This method advance the mission state, is called every loop iteration with the closest
    detected ArUco marker and its estimated distance in meters.
    """
    def update(
        self,
        detected_aruco_id: int | None,
        detected_distance_m: float | None,
    ) -> None:
        now = time.monotonic()

        # Drive toward the pickup point.
        if self.state == TaxiState.GOING_TO_PICKUP:
            if self._target_reached(
                detected_aruco_id,
                detected_distance_m,
                self.pickup_aruco_id,
            ):
                self.state = TaxiState.WAITING_AT_PICKUP
                self.stop_started_at = now
                print("Pickup reached. Stopping for 5 seconds.")

        # Remain stopped at pickup until the waiting time ends.
        elif self.state == TaxiState.WAITING_AT_PICKUP:
            if self._stop_finished(now):
                self.state = TaxiState.GOING_TO_DROPOFF
                self.stop_started_at = None
                print("Pickup stop complete. Going to dropoff.")

        # Drive toward the dropoff point.
        elif self.state == TaxiState.GOING_TO_DROPOFF:
            if self._target_reached(
                detected_aruco_id,
                detected_distance_m,
                self.dropoff_aruco_id,
            ):
                self.state = TaxiState.WAITING_AT_DROPOFF
                self.stop_started_at = now
                print("Dropoff reached. Stopping for 5 seconds.")

        # Remain stopped at dropoff until the waiting time ends.
        elif self.state == TaxiState.WAITING_AT_DROPOFF:
            if self._stop_finished(now):
                self.state = TaxiState.RETURNING_TO_PARKING
                self.stop_started_at = None
                print("Dropoff stop complete. Returning to parking.")

        # Drive toward the parking point.
        elif self.state == TaxiState.RETURNING_TO_PARKING:
            if self._target_reached(
                detected_aruco_id,
                detected_distance_m,
                self.parking_aruco_id,
            ):
                self.state = TaxiState.COMPLETE
                print("Parking reached. Robotaxi mission complete.")

    """
    ArUco 11 has two meanings:
    - Leaving parking: at <= 70 cm, enter the street on the left.
    - Outside parking: at <= 50 cm, enter parking only when
      the mission is returning to parking.
    """
    def get_aruco_11_maneuver(
        self,
        detected_aruco_id: int | None,
        detected_distance_m: float | None,
    ) -> TaxiManeuver:

        if detected_aruco_id != 11:
            self.aruco_11_armed = True
            return TaxiManeuver.NONE

        if detected_distance_m is None:
            return TaxiManeuver.NONE

        if not self.aruco_11_armed:
            return TaxiManeuver.NONE

        # Initial departure from parking.
        if (
            self.parking_exit_pending
            and detected_distance_m <= self.exit_parking_distance_m
        ):
            self.parking_exit_pending = False
            self.aruco_11_armed = False

            print(
                "ArUco 11: leaving parking "
                f"at {detected_distance_m * 100:.1f} cm."
            )

            return TaxiManeuver.ENTER_STREET_LEFT

        # Normal approach from outside the parking area.
        if detected_distance_m <= self.outside_decision_distance_m:
            self.aruco_11_armed = False

            if self.state == TaxiState.RETURNING_TO_PARKING:
                print(
                    "ArUco 11: returning to parking "
                    f"at {detected_distance_m * 100:.1f} cm."
                )

                return TaxiManeuver.ENTER_PARKING_LEFT

            print(
                "ArUco 11: staying on outside track "
                f"at {detected_distance_m * 100:.1f} cm."
            )

        return TaxiManeuver.NONE

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