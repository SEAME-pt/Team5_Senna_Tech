"""Path planner for robotaxi maneuver offsets and smooth RETURNING interpolation."""

import time


class PathPlanner:

    def __init__(
        self,
        lane_offset:       float = 0.80,
        return_duration_s: float = 1.5,
    ):
        self.lane_offset       = lane_offset
        self.return_duration_s = return_duration_s

        self._returning:     bool  = False
        self._return_start:  float = 0.0
        self._cte_at_return: float = 0.0
        self._desvio_side:   str   = "left"

        # calibration offsets for robotaxi (need to be tested!!!!!)
        self.maneuver_delay_s = 2.0
        self._maneuver_start_time = None
        self._last_state = None
        self.parking_out_duration_s = 5.0
        self.offset_parking_out_left  = -0.30  
        self.offset_parking_out_right = +0.30  
        self.offset_cross_left        = -0.90  # leaving the intersection (ArUco 13)
        self.offset_cross_right       = +0.90  # leaving the intersection (ArUco 11)
        self.offset_parking_in_left   = -0.65  # entering the intersection (ArUco 11)
        self.offset_parking_in_right  = +0.65  # entering the intersection (ArUco 12)
    
    def parking_out_complete(self) -> bool:
        """Retorna True se o tempo total estimado para a saída do parque expirou."""
        if self._maneuver_start_time is not None:
            return (time.perf_counter() - self._maneuver_start_time) >= self.parking_out_duration_s
        return False

    def calculate_target_cte(
        self,
        current_state,
    ) -> float:
        """
        Returns the target CTE to be passed to the PID in this frame.

        current_state : State of the FSM
        obstacle_side : unused in current non-avoidance mode
        """
        from decision.decision_fsm import State, TAXIROBOT_STATES

        if current_state in (State.PARKING_OUT_LEFT, State.PARKING_OUT_RIGHT):
            if self._maneuver_start_time is None:
                self._maneuver_start_time = time.perf_counter()
        else:
            self._maneuver_start_time = None

        # ── Robotaxi Maneuver Routing ────────────────────────────────────────
        if current_state == State.PARKING_OUT_LEFT:
            self._returning = False; self._desvio_side = "left"
            return self.offset_parking_out_left

        if current_state == State.PARKING_OUT_RIGHT:
            self._returning = False; self._desvio_side = "right"
            return self.offset_parking_out_right

        if current_state == State.CROSS_LEFT:
            self._returning = False; self._desvio_side = "left"
            return self.offset_cross_left

        if current_state == State.CROSS_RIGHT:
            self._returning = False; self._desvio_side = "right"
            return self.offset_cross_right

        if current_state == State.PARKING_IN_LEFT:
            self._returning = False; self._desvio_side = "left"
            return self.offset_parking_in_left

        if current_state == State.PARKING_IN_RIGHT:
            self._returning = False; self._desvio_side = "right"
            return self.offset_parking_in_right

        # ── Interpolated return ────────────────────────────────────
        if current_state == State.RETURNING:
            if not self._returning:
                self._returning     = True
                self._return_start  = time.perf_counter()
                self._cte_at_return = (
                    -self.lane_offset if self._desvio_side == "left" else +self.lane_offset
                )

            elapsed  = time.perf_counter() - self._return_start
            progress = min(1.0, elapsed / self.return_duration_s)
            return _lerp(self._cte_at_return, 0.0, progress)

        # ── Normal driving ────────────────────────────────────────
        self._returning = False
        return 0.0

    def return_complete(self) -> bool:
        """True when the return interpolation is complete."""
        if not self._returning:
            return False
        return (time.perf_counter() - self._return_start) >= self.return_duration_s

    def reset(self):
        self._returning         = False
        self._return_start      = 0.0
        self._cte_at_return     = 0.0


def _lerp(a: float, b: float, t: float) -> float:
    """Linear interpolation between a and b by factor t in [0, 1]."""
    return a + (b - a) * t
