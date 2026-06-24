"""
Responsibilities:
1. Calculate the target CTE based on the FSM state
   - Deviation states (PREPARE_AVOID, AVOIDING, BLIND_WAIT) → CTE shifted
     to the OPPOSITE side of the obstacle (determined by the ObstacleTracker)
   - RETURNING state → smoothly interpolates from the shifted CTE → 0.0
   - Remaining states → CTE = 0.0 (lane center)
2. Manage the BLIND_WAIT timer with time.time() (more accurate than frames,
   as it is independent of FPS variations)
3. Confirm when the return interpolation is complete
   (signal for the FSM to transition RETURNING → previous speed state)

Parameters
----------
lane_offset      : magnitude of the normalized deviation [0, 1].
blind_wait_time  : seconds to wait in BLIND_WAIT before returning.
return_duration_s: duration of the return-to-center interpolation.
"""

import time


class PathPlanner:

    def __init__(
        self,
        lane_offset:       float = 0.80,
        blind_wait_time:   float = 2.5,
        return_duration_s: float = 1.5,
    ):
        self.lane_offset       = lane_offset
        self.blind_wait_time   = blind_wait_time
        self.return_duration_s = return_duration_s

        self._blind_timer_start: float | None = None

        self._returning:     bool  = False
        self._return_start:  float = 0.0
        self._cte_at_return: float = 0.0
        self._desvio_side:   str   = "left"

        # calibration offsets for robotaxi (need to be tested!!!!!)
        self.offset_parking_out_left  = -0.30  
        self.offset_parking_out_right = +0.30  
        self.offset_cross_left        = -0.90  # leaving the intersection (ArUco 13)
        self.offset_cross_right       = +0.90  # leaving the intersection (ArUco 11)
        self.offset_parking_in_left   = -0.65  # entering the intersection (ArUco 11)
        self.offset_parking_in_right  = +0.65  # entering the intersection (ArUco 12)

    def calculate_target_cte(
        self,
        current_state,
        obstacle_side: str = "right",   # "left" | "right" | "center"
    ) -> float:
        """
        Returns the target CTE to be passed to the PID in this frame.

        current_state : State of the FSM
        obstacle_side : side of the obstacle in BEV (from ObstacleTracker)
        """
        from decision.decision_fsm import State

        # ── Active deviation for obstacle avoidance ──────────────────────────────────────────
        if current_state in (State.PREPARE_AVOID, State.AVOIDING, State.BLIND_WAIT):
            self._returning = False
            # Move to the opposite side of the obstacle
            if obstacle_side in ("right", "center"):
                self._desvio_side = "left"
                return -self.lane_offset        # CTE negative = turn left
            else:
                self._desvio_side = "right"
                return +self.lane_offset        # CTE positive = turn right
            
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

    def check_blind_wait_timeout(self) -> bool:
        """
        Should be called every frame when the FSM is in BLIND_WAIT.
        Starts the timer on the first call; returns True when it expires.
        """
        if self._blind_timer_start is None:
            self._blind_timer_start = time.time()
            return False
        return (time.time() - self._blind_timer_start) >= self.blind_wait_time

    def reset_blind_timer(self):
        """Should be called when the FSM exits BLIND_WAIT (for any state)."""
        self._blind_timer_start = None

    def return_complete(self) -> bool:
        """True when the return interpolation is complete."""
        if not self._returning:
            return False
        return (time.perf_counter() - self._return_start) >= self.return_duration_s

    def reset(self):
        self._blind_timer_start = None
        self._returning         = False
        self._return_start      = 0.0
        self._cte_at_return     = 0.0


def _lerp(a: float, b: float, t: float) -> float:
    """Linear interpolation between a and b by factor t in [0, 1]."""
    return a + (b - a) * t
