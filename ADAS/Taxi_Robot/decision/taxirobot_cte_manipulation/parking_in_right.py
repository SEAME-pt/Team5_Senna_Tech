"""ArUco 11 while RETURNING_TO_PARKING: blind LEFT turn into the parking ramp.

Drives State.PARKING_IN_LEFT. Same marker (ArUco 11) as parking_out_right.py;
the mission state is what tells the two apart.
"""

from decision.decision_fsm import State
from .robotaxi_mission import TaxiState


# ================= TUNING (teste real) ===============================
ARUCO_ID = 11

# Mission states in which ArUco 11 means "turn left into the parking ramp".
TRIGGER_TAXI_STATES = {TaxiState.RETURNING_TO_PARKING}

# Distance to ArUco 11 at which the blind turn starts.
TRIGGER_DISTANCE_M = 0.75
FORCED_DURATION_S = 11.1
FORCED_CTE = -0.90
FORCED_STEERING = 0.90
# =====================================================================

STATE_NAME = State.PARKING_IN_LEFT.name


class ParkingInRightPolicy:
	"""Decides when to start the ArUco-11 blind left turn into parking."""

	def should_start_forced(
		self,
		fsm_state: State,
		taxi_state: TaxiState,
		aruco_id: int | None,
		aruco_distance_m: float | None,
	) -> bool:
		# Keyed on fsm_state, not on TaxiManeuver: the mission emits the maneuver
		# once (at outside_decision_distance_m = 1.30 m) and disarms the marker,
		# so the enum is already NONE at TRIGGER_DISTANCE_M. The FSM state persists.
		return (
			fsm_state == State.PARKING_IN_LEFT
			and taxi_state in TRIGGER_TAXI_STATES
			and aruco_id == ARUCO_ID
			and aruco_distance_m is not None
			and aruco_distance_m <= TRIGGER_DISTANCE_M
		)