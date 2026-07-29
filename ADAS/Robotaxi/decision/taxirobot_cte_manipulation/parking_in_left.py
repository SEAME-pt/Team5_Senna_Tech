"""Parking-in specific state transition policy."""

from .robotaxi_mission import TaxiManeuver


# ArUco 12 trigger for parking-in-right blind maneuver.
PARKING_IN_RIGHT_TRIGGER_DISTANCE_M = 0.75
PARKING_IN_RIGHT_FORCED_DURATION_S = 6.0


class ParkingInPolicy:
	"""Decides when to leave parking-in states and return to lane-centering flow."""

	def should_transition_to_returning(self, current_state, aruco_id: int | None) -> bool:
		return current_state.name in {"PARKING_IN_LEFT", "PARKING_IN_RIGHT"} and aruco_id is None

	def should_start_parking_in_right_forced(
		self,
		taxi_maneuver: TaxiManeuver,
		aruco_id: int | None,
		aruco_distance_m: float | None,
	) -> bool:
		"""True when ArUco 12 is close enough to start parking-in-right blind turn."""
		return (
			taxi_maneuver == TaxiManeuver.PARKING_IN_RIGHT
			and aruco_id == 12
			and aruco_distance_m is not None
			and aruco_distance_m <= PARKING_IN_RIGHT_TRIGGER_DISTANCE_M
		)
