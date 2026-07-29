"""ArUco 11 while GOING_TO_PICKUP: blind RIGHT turn at the intersection.

Drives State.CROSS_RIGHT. Same marker (ArUco 11) as parking_in_right.py; the
mission state is what tells the two apart.
"""

from decision.decision_fsm import State
from .robotaxi_mission import TaxiState


# ================= TUNING (real-world test) ==========================
ARUCO_ID = 11

# Mission states in which ArUco 11 means "turn right at the crossing".
TRIGGER_TAXI_STATES = {TaxiState.GOING_TO_PICKUP}

# Distance to ArUco 11 at which the blind turn starts.
# Larger -> starts turning earlier (cuts the corner).
# Smaller -> starts turning later (goes wide).
TRIGGER_DISTANCE_M = 0.67

# Duration of the blind turn. With fixed throttle, this defines the turn radius.
FORCED_DURATION_S = 7.0

# Target CTE during the maneuver. Positive = offset to the RIGHT.
FORCED_CTE = 0.70

# Direct steering command. Negative = turn RIGHT.
FORCED_STEERING = -1.0
# =====================================================================

STATE_NAME = State.CROSS_RIGHT.name

class ParkingOutRightPolicy:
	"""Decides when to start the ArUco-11 blind right turn at the crossing."""

	def should_start_forced(
		self,
		fsm_state: State,
		taxi_state: TaxiState,
		aruco_id: int | None,
		aruco_distance_m: float | None,
	) -> bool:
		return (
			fsm_state == State.CROSS_RIGHT
			and taxi_state in TRIGGER_TAXI_STATES
			and aruco_id == ARUCO_ID
			and aruco_distance_m is not None
			and aruco_distance_m <= TRIGGER_DISTANCE_M
		)