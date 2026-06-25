from dataclasses import dataclass
from enum import Enum, auto
import time

from map.track_map import GridPos, get_aruco_id
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
    Decide the initial parking maneuver before the car starts moving.

    The first special exit marker found in the path determines which
    side of the parking station the car must use:

    ArUco 11 -> PARKING_LEFT
    ArUco 13 -> PARKING_RIGHT
    """
    def get_initial_parking_maneuver(self) -> TaxiManeuver:

        # At startup, the active goal must be the pickup point.
        if self.state != TaxiState.GOING_TO_PICKUP:
            return TaxiManeuver.NONE
    
        path = find_path(self.parking, self.pickup)
    
        if not path:
            self.state = TaxiState.FAULT
            print("Robotaxi fault: no path from parking to pickup.")
            return TaxiManeuver.NONE
    
        for pos in path[1:]:
            aruco_id = get_aruco_id(pos)
    
            # ArUco 11 is the left-side route out of parking.
            if aruco_id == 11:
                print(
                    "Startup route selected: "
                    "parking -> ArUco 11 -> PARKING_LEFT"
                )
                return TaxiManeuver.PARKING_LEFT
    
            # ArUco 13 is the right-side route out of parking.
            if aruco_id == 13:
                print(
                    "Startup route selected: "
                    "parking -> ArUco 13 -> PARKING_RIGHT"
                )
                return TaxiManeuver.PARKING_RIGHT
    
        self.state = TaxiState.FAULT
        print(
            "Robotaxi fault: path from parking to pickup "
            "does not pass through ArUco 11 or ArUco 13."
        )
    
        return TaxiManeuver.NONE

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
    - Leaving parking: at <= 70 cm, enter the street on the right.
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

            # aqui retornava TaxiManeuver.ENTER_STREET_LEFT mas aqui
            # nao é logo quando ele sai do estacionamento? ou é mesmo
            # na saída do cruzamento? e se ele esta a ver o numero 11 e é saída do cruzamento
            # nao era para ser virar a direita?
            return TaxiManeuver.CROSS_RIGHT

        # Normal approach from outside the parking area.
        if detected_distance_m <= self.outside_decision_distance_m:
            self.aruco_11_armed = False

            if self.state == TaxiState.RETURNING_TO_PARKING:
                print(
                    "ArUco 11: returning to parking "
                    f"at {detected_distance_m * 100:.1f} cm."
                )

                return TaxiManeuver.PARKING_IN_LEFT

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