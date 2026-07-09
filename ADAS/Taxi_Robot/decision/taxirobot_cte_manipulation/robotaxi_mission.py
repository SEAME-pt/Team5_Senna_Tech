from dataclasses import dataclass
from enum import Enum, auto
import time

from decision.decision_fsm import State
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

class TaxiManeuver(Enum):
    NONE = auto()
    PARKING_OUT_LEFT = auto()
    PARKING_OUT_RIGHT = auto()
    CROSS_LEFT = auto()
    CROSS_RIGHT = auto()
    PARKING_IN_LEFT = auto()
    PARKING_IN_RIGHT = auto()


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
    stop_distance_m: float = 0.25

    stop_duration_s: float = 5.0
    stop_started_at: float | None = None

    # ArUco-based decision thresholds.
    outside_decision_distance_m: float = 1.30
    cross_left_trigger_distance_m: float = 0.65
    startup_decision_aruco_id: int = 14
    parking_station_stop_distance_m: float = 0.20

    # True only at the start of the mission.
    parking_exit_pending: bool = True
    expected_start_cross_aruco_id: int | None = None

    # Prevents repeating the same action every frame.
    aruco_armed: bool = True

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

    # Return the route from the current position to the mission goal.
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
                self.parking_station_stop_distance_m,
            ):
                self.state = TaxiState.COMPLETE
                print("Parking reached. Robotaxi mission complete.")

    def get_taxi_maneuver(
        self,
        detected_aruco_id: int | None,
        detected_distance_m: float | None,
        path: list = None
    ) -> TaxiManeuver:

        # The first left/right decision only happens when ArUco 14 is seen close enough.
        if self.parking_exit_pending:
            if (
                detected_aruco_id != self.startup_decision_aruco_id
                or detected_distance_m is None
                or detected_distance_m > self.outside_decision_distance_m
            ):
                return TaxiManeuver.NONE

            self.parking_exit_pending = False

            if not path or len(path) <= 1:
                return TaxiManeuver.NONE

            # The first path cells may keep the same parking column before the split.
            # Decide startup side from the first horizontal deviation in the route.
            startup_col = _first_col_deviation(path=path, base_col=self.parking.col)
            if startup_col is None:
                return TaxiManeuver.NONE

            if startup_col < self.parking.col:
                self.expected_start_cross_aruco_id = 11
                print("Startup ArUco 14 detected: path goes RIGHT.")
                return TaxiManeuver.PARKING_OUT_RIGHT

            self.expected_start_cross_aruco_id = 13
            print("Startup ArUco 14 detected: path goes LEFT.")
            return TaxiManeuver.PARKING_OUT_LEFT

        if detected_aruco_id is None or detected_distance_m is None:
            self.aruco_armed = True
            return TaxiManeuver.NONE

        if not self.aruco_armed or detected_distance_m > self.outside_decision_distance_m:
            return TaxiManeuver.NONE

        # After leaving parking, only accept the crossing marker that matches
        # the direction chosen at ArUco 14.
        if self.expected_start_cross_aruco_id is not None:
            if detected_aruco_id != self.expected_start_cross_aruco_id:
                return TaxiManeuver.NONE

            self.expected_start_cross_aruco_id = None

        # ── GEOGRAPHIC MAPPING OF THE ARUCOS ──────────────────────────
        
        # ArUco 11: Turn right onto the intersection on the way there, or turn left onto the park entrance on the way back.
        if detected_aruco_id == 11:
            self.aruco_armed = False
            if self.state == TaxiState.RETURNING_TO_PARKING:
                return TaxiManeuver.PARKING_IN_LEFT
            else:
                return TaxiManeuver.CROSS_RIGHT

        # ArUco 12: Turn right onto the parking entrance on the way back.
        if detected_aruco_id == 12 and self.state == TaxiState.RETURNING_TO_PARKING:
            self.aruco_armed = False
            return TaxiManeuver.PARKING_IN_RIGHT

        # ArUco 13: Turn left only when close enough to the marker.
        if (
            detected_aruco_id == 13
            and detected_distance_m <= self.cross_left_trigger_distance_m
        ):
            self.aruco_armed = False
            return TaxiManeuver.CROSS_LEFT

        return TaxiManeuver.NONE

    def orchestrate_maneuver(
        self,
        fsm,
        taxi_maneuver: TaxiManeuver,
        aruco_id: int | None,
    ) -> None:
        """Apply non-startup maneuver transitions to the FSM.

        Startup parking-out left/right decision (ArUco 14 event)
        """
        if taxi_maneuver == TaxiManeuver.CROSS_LEFT:
            fsm.signal_robotaxi_state(State.CROSS_LEFT, "ArUco 13: Executing cross left")
            return

        if taxi_maneuver == TaxiManeuver.CROSS_RIGHT:
            fsm.signal_robotaxi_state(State.CROSS_RIGHT, "ArUco 11 detected: leaving crossing")
            return

        if taxi_maneuver == TaxiManeuver.PARKING_IN_LEFT:
            fsm.signal_robotaxi_state(State.PARKING_IN_LEFT, "ArUco 11 detected: entering parking")
            return

        if taxi_maneuver == TaxiManeuver.PARKING_IN_RIGHT:
            fsm.signal_robotaxi_state(State.PARKING_IN_RIGHT, "ArUco 12: Approaching parking from right")
            return

        if fsm.state in (State.PARKING_IN_LEFT, State.PARKING_IN_RIGHT) and aruco_id is None:
            fsm.state = State.SPEED_50

    def _target_reached(
        self,
        detected_aruco_id: int | None,
        detected_distance_m: float | None,
        target_aruco_id: int,
        max_distance_m: float | None = None,
    ) -> bool:
        if detected_aruco_id is None or detected_distance_m is None:
            return False

        if max_distance_m is None:
            max_distance_m = self.stop_distance_m

        return (
            detected_aruco_id == target_aruco_id
            and detected_distance_m <= max_distance_m
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


def _first_col_deviation(path: list[GridPos], base_col: int) -> int | None:
    for pos in path[1:]:
        if pos.col != base_col:
            return pos.col
    return None
