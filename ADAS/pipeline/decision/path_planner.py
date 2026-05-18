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
lane_offset : magnitude of the normalized deviation [0, 1].
170 px width → 65 px ≈ 0.38 normalized.
blind_wait_time: seconds to wait in BLIND_WAIT before returning.
return_duration_s: duration of the return-to-center interpolation.
"""

import time


class PathPlanner:

    def __init__(
        self,
        lane_offset:       float = 0.38,
        blind_wait_time:   float = 2.5,
        return_duration_s: float = 1.5,
    ):
        self.lane_offset       = lane_offset
        self.blind_wait_time   = blind_wait_time
        self.return_duration_s = return_duration_s

        # Timer of blind wait
        self._blind_timer_start: float | None = None

        # Return interpolation state
        self._returning:       bool  = False
        self._return_start:    float = 0.0
        self._cte_at_return:   float = 0.0

        # Side of the current deviation ("left" | "right")
        self._desvio_side: str = "left"

    # ──────────────────────────────────────────────────────────────
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

        # ── Active deviation──────────────────────────────────────────
        if current_state in (
            State.PREPARE_AVOID,
            State.AVOIDING,
            State.BLIND_WAIT,
        ):
            self._returning = False

            # Move to the opposite side of the obstacle.
            if obstacle_side in ("right", "center"):
                self._desvio_side = "left"
                return -self.lane_offset        # CTE negative = turn left
            else:
                self._desvio_side = "right"
                return +self.lane_offset        # CTE positive = turn right

        # ── Interpolated return ────────────────────────────────────
        if current_state == State.RETURNING:
            if not self._returning:
                self._returning    = True
                self._return_start = time.perf_counter()
                # Target CTE at return start = displaced position
                self._cte_at_return = (
                    -self.lane_offset
                    if self._desvio_side == "left"
                    else +self.lane_offset
                )

            elapsed  = time.perf_counter() - self._return_start
            progress = min(1.0, elapsed / self.return_duration_s)
            return _lerp(self._cte_at_return, 0.0, progress)

        # ── Normal driving ────────────────────────────────────────
        self._returning = False
        return 0.0

    # ──────────────────────────────────────────────────────────────
    def check_blind_wait_timeout(self) -> bool:
        """
        It should be called every frame when the FSM is in BLIND_WAIT.
        Starts the timer on the first call; returns True when it expires.
        """
        if self._blind_timer_start is None:
            self._blind_timer_start = time.time()
            return False
        return (time.time() - self._blind_timer_start) >= self.blind_wait_time

    def reset_blind_timer(self):
        """It should be called when the FSM exits BLIND_WAIT (for any state)."""
        self._blind_timer_start = None

    # ──────────────────────────────────────────────────────────────
    def return_complete(self) -> bool:
        """True when the return interpolation is complete."""
        if not self._returning:
            return False
        elapsed = time.perf_counter() - self._return_start
        return elapsed >= self.return_duration_s

    def reset(self):
        self._blind_timer_start = None
        self._returning         = False
        self._return_start      = 0.0
        self._cte_at_return     = 0.0


# ── helpers ────────────────────────────────────────────────────────────

def _lerp(a: float, b: float, t: float) -> float:
    return a + (b - a) * t
