"""Parking-in specific state transition policy."""


class ParkingInPolicy:
	"""Decides when to leave parking-in states and return to lane-centering flow."""

	def should_transition_to_returning(self, current_state, aruco_id: int | None) -> bool:
		return current_state.name in {"PARKING_IN_LEFT", "PARKING_IN_RIGHT"} and aruco_id is None
