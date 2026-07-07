"""Path planner for robotaxi maneuver offsets and smooth RETURNING interpolation."""

import time


class PathPlanner:

    def __init__(
        self,
        # Variables for RETURNING interpolation
        lane_offset:       float = 0.80,
        return_duration_s: float = 1.5,
    ):
        self.lane_offset       = lane_offset
        self.return_duration_s = return_duration_s

        self._returning:     bool  = False
        self._return_start:  float = 0.0
        self._cte_at_return: float = 0.0
        self._deviation_side: str  = "left"

        # Time gate for parking-out completion logic used by main.
        self._maneuver_start_time = None
        self._last_state = None

        # Time duration for parking-out maneuver to be considered complete.
        self.parking_out_duration_s = 5.0

        # Blindly force CTE for a fixed duration
        self.forced_maneuver_duration_s = 5.0
        self._active_forced_maneuver_duration_s = self.forced_maneuver_duration_s

        self._forced_maneuver_state_name: str | None = None
        self._forced_maneuver_started_at: float | None = None

        # Add new states here as needed !!!!
        # Keep forced CTE values by maneuver-state name.
        self.maneuver_cte_by_state = {
            "PARKING_OUT_LEFT": -1.0,
            "CROSS_LEFT": -1.0,
            "CROSS_RIGHT": 1.0,
        }

        # States whose CTE bias must only be active during forced window.
        self.cte_only_during_forced_states = {
            "PARKING_OUT_LEFT",
            "CROSS_LEFT",
            "CROSS_RIGHT",
        }

        # Optional direct steering override while a forced maneuver is active.
        self.forced_steering_by_state = {
            "PARKING_OUT_LEFT": 1.0,
            "CROSS_LEFT": 1.0,
            "CROSS_RIGHT": -0.85,
        }

    def start_forced_maneuver(self, state_name: str, duration_s: float | None = None) -> None:
        if state_name not in self.maneuver_cte_by_state:
            return

        self._forced_maneuver_state_name = state_name
        self._forced_maneuver_started_at = time.perf_counter()
        if duration_s is None:
            self._active_forced_maneuver_duration_s = self.forced_maneuver_duration_s
        else:
            self._active_forced_maneuver_duration_s = duration_s

    def is_forced_maneuver_active(self) -> bool:
        if (
            self._forced_maneuver_state_name is None
            or self._forced_maneuver_started_at is None
        ):
            return False

        elapsed = time.perf_counter() - self._forced_maneuver_started_at
        if elapsed < self._active_forced_maneuver_duration_s:
            return True

        self._forced_maneuver_state_name = None
        self._forced_maneuver_started_at = None
        self._active_forced_maneuver_duration_s = self.forced_maneuver_duration_s
        return False

    def forced_maneuver_state_name(self) -> str | None:
        if self.is_forced_maneuver_active():
            return self._forced_maneuver_state_name
        return None

    def forced_steering_override(self) -> float | None:
        state_name = self.forced_maneuver_state_name()
        if state_name is None:
            return None
        return self.forced_steering_by_state.get(state_name)

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
        """
        from decision.decision_fsm import State

        if current_state in (State.PARKING_OUT_LEFT, State.PARKING_OUT_RIGHT):
            if self._maneuver_start_time is None:
                self._maneuver_start_time = time.perf_counter()
        else:
            self._maneuver_start_time = None

        forced_state_name = self.forced_maneuver_state_name()
        if forced_state_name is not None:
            maneuver_cte = self.maneuver_cte_by_state[forced_state_name]
            self._returning = False
            self._deviation_side = "left" if maneuver_cte < 0.0 else "right"
            return maneuver_cte

        if current_state.name in self.cte_only_during_forced_states:
            maneuver_cte = None
        else:
            maneuver_cte = self.maneuver_cte_by_state.get(current_state.name)

        if maneuver_cte is not None:
            self._returning = False
            self._deviation_side = "left" if maneuver_cte < 0.0 else "right"
            return maneuver_cte

        # ── Interpolated return ────────────────────────────────────
        if current_state == State.RETURNING:
            if not self._returning:
                self._returning     = True
                self._return_start  = time.perf_counter()
                self._cte_at_return = (
                    -self.lane_offset if self._deviation_side == "left" else +self.lane_offset
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
        self._forced_maneuver_state_name = None
        self._forced_maneuver_started_at = None
        self._active_forced_maneuver_duration_s = self.forced_maneuver_duration_s


def _lerp(a: float, b: float, t: float) -> float:
    """Linear interpolation between a and b by factor t in [0, 1]."""
    return a + (b - a) * t
