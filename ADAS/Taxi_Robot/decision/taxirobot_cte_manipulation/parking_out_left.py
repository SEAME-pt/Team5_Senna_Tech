"""Parking-out and CTE profile primitives used by the taxi robot controller."""

import time

from decision.decision_fsm import State


class ForcedManeuverWindow:
	"""Tracks fixed-duration forced maneuver windows and optional steering overrides."""

	def __init__(self):
		self.default_duration_s = 3.0
		self._active_duration_s = self.default_duration_s
		self._state_name = None
		self._started_at = None

		# forced maneuver CTE and steering overrides by state name.
		self.maneuver_cte_by_state = {
			"PARKING_OUT_LEFT": -1.0,
			"CROSS_LEFT": -0.60,
			"PARKING_IN_RIGHT": -0.70,
		}

		self.forced_steering_by_state = {
			"PARKING_OUT_LEFT": 1.0,
			"CROSS_LEFT": 1.0,
			"PARKING_IN_RIGHT": -0.70,
		}

	def start(self, state_name: str, duration_s: float | None = None) -> None:
		if state_name not in self.maneuver_cte_by_state:
			return

		self._state_name = state_name
		self._started_at = time.perf_counter()
		self._active_duration_s = self.default_duration_s if duration_s is None else duration_s

	def is_active(self) -> bool:
		if self._state_name is None or self._started_at is None:
			return False

		if (time.perf_counter() - self._started_at) < self._active_duration_s:
			return True

		self._state_name = None
		self._started_at = None
		self._active_duration_s = self.default_duration_s
		return False

	def state_name(self) -> str | None:
		if self.is_active():
			return self._state_name
		return None

	def steering_override(self) -> float | None:
		state_name = self.state_name()
		if state_name is None:
			return None
		return self.forced_steering_by_state.get(state_name)

	def forced_cte(self) -> float | None:
		state_name = self.state_name()
		if state_name is None:
			return None
		return self.maneuver_cte_by_state.get(state_name)

	def reset(self) -> None:
		self._state_name = None
		self._started_at = None
		self._active_duration_s = self.default_duration_s


class ParkingOutLeftPolicy:
	"""Encapsulates parking-out-left specific ArUco decisions."""

	def apply_cross_left_transition(
		self,
		fsm,
		aruco_id: int | None,
		aruco_distance_m: float | None,
		cross_left_forced_trigger_m: float,
	) -> bool:
		"""Switch to CROSS_LEFT and tell caller whether forced window should start."""
		changed = fsm.signal_robotaxi_state(State.CROSS_LEFT, "ArUco 13: Executing cross left")
		return (
			changed
			and aruco_id == 13
			and aruco_distance_m is not None
			and aruco_distance_m <= cross_left_forced_trigger_m
		)


class ParkingOutTimer:
	"""Tracks parking-out elapsed time so main does not carry this logic."""

	def __init__(self, duration_s: float = 3.5):
		self.duration_s = duration_s
		self._start_time = None

	def update(self, in_parking_out_state: bool) -> None:
		if in_parking_out_state:
			if self._start_time is None:
				self._start_time = time.perf_counter()
			return
		self._start_time = None

	def complete(self) -> bool:
		if self._start_time is None:
			return False
		return (time.perf_counter() - self._start_time) >= self.duration_s

	def reset(self) -> None:
		self._start_time = None

class ReturningProfile:
	"""Provides smooth interpolation from maneuver CTE back to lane center."""

	def __init__(self, lane_offset: float = 0.70, return_duration_s: float = 1.5):
		self.lane_offset = lane_offset
		self.return_duration_s = return_duration_s

		self._returning = False
		self._return_start = 0.0
		self._cte_at_return = 0.0
		self._deviation_side = "left"

	def update_deviation_side(self, maneuver_cte: float) -> None:
		self._returning = False
		self._deviation_side = "left" if maneuver_cte < 0.0 else "right"

	def target_cte_for_returning(self, is_returning_state: bool) -> float | None:
		if not is_returning_state:
			self._returning = False
			return None

		if not self._returning:
			self._returning = True
			self._return_start = time.perf_counter()
			self._cte_at_return = -self.lane_offset if self._deviation_side == "left" else self.lane_offset

		elapsed = time.perf_counter() - self._return_start
		progress = min(1.0, elapsed / self.return_duration_s)
		return _lerp(self._cte_at_return, 0.0, progress)

	def return_complete(self) -> bool:
		if not self._returning:
			return False
		return (time.perf_counter() - self._return_start) >= self.return_duration_s

	def reset(self) -> None:
		self._returning = False
		self._return_start = 0.0
		self._cte_at_return = 0.0


def _lerp(a: float, b: float, t: float) -> float:
	return a + (b - a) * t
