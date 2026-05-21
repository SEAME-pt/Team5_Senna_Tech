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

    def calculate_target_cte(
        self,
        current_state,
        obstacle_side: str = "right",
    ) -> float:
        from decision.decision_fsm import State

        if current_state in (State.PREPARE_AVOID, State.AVOIDING, State.BLIND_WAIT):
            self._returning = False
            if obstacle_side in ("right", "center"):
                self._desvio_side = "left"
                return -self.lane_offset
            else:
                self._desvio_side = "right"
                return +self.lane_offset

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

        self._returning = False
        return 0.0

    def check_blind_wait_timeout(self) -> bool:
        if self._blind_timer_start is None:
            self._blind_timer_start = time.time()
            return False
        return (time.time() - self._blind_timer_start) >= self.blind_wait_time

    def reset_blind_timer(self):
        self._blind_timer_start = None

    def return_complete(self) -> bool:
        if not self._returning:
            return False
        return (time.perf_counter() - self._return_start) >= self.return_duration_s

    def reset(self):
        self._blind_timer_start = None
        self._returning         = False
        self._return_start      = 0.0
        self._cte_at_return     = 0.0


def _lerp(a: float, b: float, t: float) -> float:
    return a + (b - a) * t
