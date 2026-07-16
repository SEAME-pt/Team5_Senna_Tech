# Robotaxi — Documentation

This document describes the **Robotaxi** subsystem: the logic that decides, throughout a mission (parking → pickup → dropoff → parking), which phase of the mission the car is in, which route to follow on the map grid, and which driving maneuver should be executed at any given moment, based on the estimated position and the detected ArUco markers.

---

## 1. Architecture overview

```
track_map.py                   ← map grid, cells, ArUco IDs per position
path.py                        ← pathfinding (BFS) and text-based map printing

RobotaxiMission                ← mission state machine (pickup/dropoff/parking)
    └── TaxiState / TaxiManeuver                          (robotaxi_mission.py)

TaxiRobotCTEController         ← orchestrates forced maneuvers and computes the target CTE
    ├── ForcedManeuverWindow       (parking_out_left.py)
    ├── ParkingOutTimer            (parking_out_left.py)
    ├── ReturningProfile           (parking_out_left.py)
    ├── ParkingInPolicy            (parking_in_left.py)      → PARKING_IN_RIGHT (ArUco 12)
    ├── ParkingOutRightPolicy      (parking_out_right.py)    → CROSS_RIGHT (ArUco 11, outbound)
    └── ParkingInRightPolicy       (parking_in_right.py)     → PARKING_IN_LEFT (ArUco 11, inbound)
```

Two state machines coexist and communicate with each other:

- **`RobotaxiMission` / `TaxiState`** — "where am I in the mission" (heading to pickup, waiting, heading to dropoff, returning…).
- **`VehicleFSM` / `State`** (`decision_fsm` module, external to this subsystem) — "which driving maneuver am I executing right now" (lane following, crossing left/right, entering/exiting parking, etc.).

`TaxiRobotCTEController` bridges the two: it translates mission decisions (`TaxiManeuver`) into `VehicleFSM` transitions and into forced CTE (Cross-Track Error) values, so the car literally turns at the right intersections even when the lane isn't reliable.

> **Note on file names:** `parking_in_right.py` and `parking_out_right.py` have names that don't exactly match what they do. `parking_out_right.py` defines `ParkingOutRightPolicy`, which actually triggers `CROSS_RIGHT` (a right turn at an intersection, on the way to the destination). `parking_in_right.py` defines `ParkingInRightPolicy`, which actually triggers `PARKING_IN_LEFT` (a left turn into parking, on the way back). Both react to the **same ArUco marker 11**; it's the mission's `TaxiState` (`GOING_TO_PICKUP`/`GOING_TO_DROPOFF` vs `RETURNING_TO_PARKING`) that tells the two apart.

---

## 2. `track_map.py` — map grid

Defines the track map as a 2D matrix (`TRACK_MAP`, 19 rows × 15 columns) of `Cell` values:

| Cell | Value | Meaning |
|---|---|---|
| `ROAD` | 0 | Normal road (drivable) |
| `BLOCKED` | 1 | Blocked (not drivable) |
| `CROSSING` | 2 | Crosswalk/crossing (drivable) |
| `ARUCO` | 5 | Cell with an ArUco marker (drivable) |

### `GridPos`
Immutable dataclass (`frozen=True`) with `row`/`col` — used as the position key throughout the subsystem.

### ArUco ↔ position mapping
`ARUCO_ID_BY_POS` maps each `GridPos` that carries a marker to its ID (0–15), and `ARUCO_POS_BY_ID` is the reverse mapping. The IDs relevant to maneuvers:

| ArUco ID | Position | Role in the mission |
|---|---|---|
| 11 | `(18, 6)` | `CROSS_RIGHT` (outbound) / `PARKING_IN_LEFT` (inbound) |
| 12 | `(18, 9)` | `PARKING_IN_RIGHT` |
| 13 | `(18, 11)` | `CROSS_LEFT` |
| 14 | `(15, 8)` | Startup decision (`PARKING_OUT_LEFT`/`PARKING_OUT_RIGHT`) |
| 15 | `(10, 8)` | Parking station (`PARKING_POS`) |

`PARKING_POS = GridPos(10, 8)` and `PARKING_ARUCO_ID` are derived directly from this mapping.

### Helper functions
- **`get_grid_pos_from_aruco_id(aruco_id)`** / **`get_aruco_id(pos)`** — ID ↔ position conversion.
- **`is_inside(pos)`** — checks whether the position is within the grid bounds.
- **`is_drivable(pos)`** — true if the position is within bounds and the cell is `ROAD`, `CROSSING`, or `ARUCO`.

---

## 3. `path.py` — route computation and visualization

### `find_path(start, goal)`
Pathfinding via **BFS** (breadth-first search, not A*) over the `track_map` grid:
- `get_neighbors(pos)` expands the 4 cardinal directions (`DIRECTIONS`), keeping only `is_drivable` cells.
- The search keeps a `came_from` map to reconstruct the shortest path (in number of cells) from `start` to `goal`.
- Returns an empty list `[]` if the goal is unreachable.

### `print_path_map(path, current_pos, goal_pos, pickup, dropoff)`
Prints an ASCII representation of the map to the terminal, useful for real-time debugging:

| Symbol | Meaning |
|---|---|
| `#` | Blocked |
| `.` | Road |
| `*` | Cell on the computed path |
| `A` | ArUco marker |
| `R` | Crossing/crosswalk |
| `C` | Car's current position |
| `G` | Current goal |
| `P` | Pickup |
| `D` | Dropoff |

Drawing priority per cell is: car > goal > pickup > dropoff > path > base cell type.

---

## 4. `robotaxi_mission.py` — mission state machine

### `TaxiState` (enum)
| State | Meaning |
|---|---|
| `DISABLED` | Robotaxi inactive |
| `GOING_TO_PICKUP` | Heading to the pickup point |
| `WAITING_AT_PICKUP` | Stopped at pickup (waits `stop_duration_s`) |
| `GOING_TO_DROPOFF` | Heading to the destination |
| `WAITING_AT_DROPOFF` | Stopped at dropoff |
| `RETURNING_TO_PARKING` | Returning to parking |
| `COMPLETE` | Mission finished |
| `FAULT` | Error state (not implemented in this file) |

### `TaxiManeuver` (enum)
Discrete maneuvers generated by ArUco events: `PARKING_OUT_LEFT`, `PARKING_OUT_RIGHT`, `CROSS_LEFT`, `CROSS_RIGHT`, `PARKING_IN_LEFT`, `PARKING_IN_RIGHT`, and `NONE` (no action).

### `RobotaxiMission` (dataclass)
Holds the mission configuration (parking/pickup/dropoff positions and ArUco IDs) and the current state.

Main methods:

- **`get_current_goal()`** — returns the target position based on the current `TaxiState` (pickup, dropoff, parking, or `None`).
- **`get_path(current_pos)`** — uses `find_path` (BFS, `path.py`) to compute the route to the current goal.
- **`update(detected_aruco_id, detected_distance_m)`** — advances `TaxiState`:
  - `GOING_TO_PICKUP → WAITING_AT_PICKUP` when the pickup's ArUco is seen at ≤ `stop_distance_m`.
  - `WAITING_AT_PICKUP → GOING_TO_DROPOFF` after `stop_duration_s` (3.5 s).
  - `GOING_TO_DROPOFF → WAITING_AT_DROPOFF` when the dropoff's ArUco is reached.
  - `WAITING_AT_DROPOFF → RETURNING_TO_PARKING` after the waiting time.
  - `RETURNING_TO_PARKING → COMPLETE` when the parking's ArUco is reached (uses `parking_station_stop_distance_m`).
- **`get_taxi_maneuver(detected_aruco_id, detected_distance_m, path)`** — the most complex logic in the file:
  1. **Startup decision** (`parking_exit_pending=True`): only made once ArUco 14 (`startup_decision_aruco_id`) is seen at ≤ `outside_decision_distance_m`. It looks at the first column deviation in `path` (`_first_col_deviation`) to decide whether the parking exit is to the left or right, and sets `expected_start_cross_aruco_id` (11 for right, 13 for left) to filter the next event.
  2. **ArUco "arming"** (`aruco_armed`): prevents the same maneuver from firing repeatedly while the marker stays visible; it only re-arms once the ArUco is no longer detected.
  3. **Fixed geographic mapping of the ArUcos**:
     - **ArUco 11** → `CROSS_RIGHT` (outbound) or `PARKING_IN_LEFT` (inbound).
     - **ArUco 12** → `PARKING_IN_RIGHT` (inbound only).
     - **ArUco 13** → `CROSS_LEFT`, but only once it's already at ≤ `cross_left_trigger_distance_m` (closer, for more precision).

  This method **fires the maneuver only once**, at the wider detection range (`outside_decision_distance_m` = 1.30 m), and immediately disarms (`aruco_armed = False`) — this is why the blind policies for ArUco 11 (`ParkingOutRightPolicy`/`ParkingInRightPolicy`) can't rely on `TaxiManeuver` to decide *when* to start the blind turn (see section 6): by then the enum is already back to `NONE`. Instead, those policies "listen" to the `fsm_state` already set by `orchestrate_maneuver`, and rely on a second, closer reading of the same ArUco 11.
- **`orchestrate_maneuver(fsm, taxi_maneuver, aruco_id)`** — translates `TaxiManeuver` (except the startup ones, handled in the controller) into `fsm.signal_robotaxi_state(...)`. Also resets the FSM to `SPEED_50` when leaving a parking-entry maneuver and the ArUco is no longer seen.
- **`should_stop()`** — `True` in `WAITING_AT_PICKUP`, `WAITING_AT_DROPOFF`, and `COMPLETE`.
- **`get_wait_remaining()`** — remaining stop time, for logging.

---

## 5. `parking_out_left.py` — forced maneuver primitives

### `ForcedManeuverWindow`
Manages fixed-duration time windows during which CTE and/or steering are **forced**, overriding the normal PID — used for "blind" maneuvers (unreliable lane, e.g., intersections).

- `maneuver_cte_by_state` / `forced_steering_by_state` — map state names to fixed CTE/steering values. By default they include `PARKING_OUT_LEFT`, `CROSS_LEFT`, and `PARKING_IN_RIGHT`; `TaxiRobotCTEController` dynamically registers two more entries (`CROSS_RIGHT` and `PARKING_IN_LEFT`) at startup, coming from `parking_out_right.py` and `parking_in_right.py` (see section 8).
- `start(state_name, duration_s)` — starts the window (only accepts names already present in `maneuver_cte_by_state`).
- `is_active()` — true while not expired; expires automatically and clears the state.
- `state_name()` / `steering_override()` / `forced_cte()` — accessors gated by `is_active()`.

### `ParkingOutLeftPolicy`
Applies the `CROSS_LEFT` transition on the FSM and reports whether a forced window should additionally be started (when ArUco 13 is close enough).

### `ParkingOutTimer`
Simple watchdog: measures how long the car has been in `PARKING_OUT_LEFT`/`PARKING_OUT_RIGHT` and signals `complete()` after `duration_s` (default 4.0 s, used with 3.5 s in the controller) — a safeguard against getting stuck in the exit maneuver.

### `ReturningProfile`
Smoothly interpolates the CTE back to lane center after a lateral maneuver:
- `update_deviation_side(maneuver_cte)` — records whether the deviation was to the left or right.
- `target_cte_for_returning(is_returning_state)` — during the `RETURNING` state, linearly *lerps* the CTE from the deviation back to 0 over `return_duration_s`.
- `return_complete()` — indicates when the interpolation has finished.

---

## 6. `parking_in_left.py` — right-side parking-entry policy

```python
PARKING_IN_RIGHT_TRIGGER_DISTANCE_M = 0.75
PARKING_IN_RIGHT_FORCED_DURATION_S = 6.0
```

### `ParkingInPolicy`
- **`should_transition_to_returning(current_state, aruco_id)`** — true when the car is in `PARKING_IN_LEFT` or `PARKING_IN_RIGHT` and no ArUco is visible anymore (a sign that the blind maneuver has ended and the car should return to normal lane-centering flow).
- **`should_start_parking_in_right_forced(taxi_maneuver, aruco_id, aruco_distance_m)`** — true only when:
  - the decided maneuver is `PARKING_IN_RIGHT`,
  - the ArUco seen is 12,
  - and the distance is ≤ `PARKING_IN_RIGHT_TRIGGER_DISTANCE_M` (0.75 m).

  When true, the controller starts a **6-second** forced window (`PARKING_IN_RIGHT_FORCED_DURATION_S`) with fixed CTE/steering, to blindly enter parking from the right.

  Unlike the ArUco-11 policies (section 8), this one still relies directly on `TaxiManeuver` — because ArUco 12 is only relevant in a single mission direction (`RETURNING_TO_PARKING`), so there's no ambiguity to resolve.

---

## 7. `parking_out_right.py` — right turn at the intersection (ArUco 11, outbound)

Reacts to ArUco 11 while the mission is in `GOING_TO_PICKUP` (`TRIGGER_TAXI_STATES = {TaxiState.GOING_TO_PICKUP}`), triggering `State.CROSS_RIGHT`.

### Tuning constants
| Constant | Value | Effect |
|---|---|---|
| `ARUCO_ID` | 11 | Observed marker |
| `TRIGGER_DISTANCE_M` | 0.67 m | Distance at which the blind turn starts (higher → starts turning earlier/cuts the corner; lower → passes wider) |
| `FORCED_DURATION_S` | 7.0 s | Duration of the blind turn (with fixed throttle, this sets the effective turn radius) |
| `FORCED_CTE` | 0.70 | Target CTE during the maneuver (positive = deviation to the **right**) |
| `FORCED_STEERING` | -1.0 | Direct steering command (negative = turn **right**) |

### `ParkingOutRightPolicy.should_start_forced(fsm_state, taxi_state, aruco_id, aruco_distance_m)`
True only when **all** of the following hold:
- `fsm_state == State.CROSS_RIGHT` (the FSM has already been set to this state by `orchestrate_maneuver`, at a larger distance),
- `taxi_state` is in `TRIGGER_TAXI_STATES` (i.e., `GOING_TO_PICKUP`),
- the detected ArUco is 11,
- and the distance is ≤ `TRIGGER_DISTANCE_M`.

This policy is **keyed on `fsm_state`, not on `TaxiManeuver`**: the mission has already emitted the maneuver once (at `outside_decision_distance_m` = 1.30 m) and disarmed the marker, so the `TaxiManeuver` enum is already back to `NONE` by the time the car reaches `TRIGGER_DISTANCE_M` (0.67 m). The FSM state, unlike the maneuver enum, persists — which is what allows the policy to correctly decide when to start the blind turn.

---

## 8. `parking_in_right.py` — left turn into parking (ArUco 11, inbound)

Reacts to the **same ArUco marker 11**, but while the mission is in `RETURNING_TO_PARKING` (`TRIGGER_TAXI_STATES = {TaxiState.RETURNING_TO_PARKING}`), triggering `State.PARKING_IN_LEFT`.

### Tuning constants
| Constant | Value | Effect |
|---|---|---|
| `ARUCO_ID` | 11 | Observed marker |
| `TRIGGER_DISTANCE_M` | 0.75 m | Distance at which the blind turn starts |
| `FORCED_DURATION_S` | 10.0 s | Duration of the blind turn |
| `FORCED_CTE` | -0.90 | Target CTE during the maneuver (negative = deviation to the **left**) |
| `FORCED_STEERING` | 0.90 | Direct steering command (positive = turn **left**) |

### `ParkingInRightPolicy.should_start_forced(fsm_state, taxi_state, aruco_id, aruco_distance_m)`
Same structure as the previous policy, but checks `fsm_state == State.PARKING_IN_LEFT` and `taxi_state in {RETURNING_TO_PARKING}`. Uses the same reasoning of keying on `fsm_state` instead of `TaxiManeuver`, for the same reason explained in section 7.

> These two policies (7 and 8) resolve the ambiguity of ArUco 11 being shared between two opposite maneuvers (turning right at an intersection vs. turning left into parking): the `fsm_state` has already been correctly decided by `RobotaxiMission.get_taxi_maneuver` based on `TaxiState`, and each policy simply confirms it's still in the right state once the ArUco gets close enough for the blind maneuver.

---

## 9. `taxi_robot_cte_controller.py` — central orchestrator

`TaxiRobotCTEController` class, composed of the pieces above:

| Component | Role |
|---|---|
| `ForcedManeuverWindow` | fixed-duration window with locked CTE/steering |
| `ParkingOutTimer` | safety timeout for exiting parking |
| `ReturningProfile` | interpolation back to lane center |
| `ParkingInPolicy` | trigger rule for parking-in from the right (ArUco 12) |
| `ParkingOutRightPolicy` | trigger rule for cross-right (ArUco 11, outbound) |
| `ParkingInRightPolicy` | trigger rule for parking-in from the left (ArUco 11, inbound) |

In `__init__`, the configurations from `parking_out_right.py` and `parking_in_right.py` are **dynamically registered** into `ForcedManeuverWindow`'s tables:

```python
for cfg in (cross_right_cfg, parking_in_left_cfg):
    self._forced.maneuver_cte_by_state[cfg.STATE_NAME] = cfg.FORCED_CTE
    self._forced.forced_steering_by_state[cfg.STATE_NAME] = cfg.FORCED_STEERING
```

This means all the tuning (trigger distance, duration, CTE, steering) for `CROSS_RIGHT` and `PARKING_IN_LEFT` lives exclusively in their respective modules (`parking_out_right.py`, `parking_in_right.py`), with no duplication in the controller.

### Main methods

- **`update_startup_parking_decision(fsm, taxi_maneuver)`**
  Only the startup decision (left vs. right when exiting parking):
  - `PARKING_OUT_LEFT` → changes the FSM and **starts a forced window** (fixed CTE/steering, left bias).
  - `PARKING_OUT_RIGHT` → changes the FSM but **does not force CTE** (stays lane-centered).
  - When the forced window ends (or `ParkingOutTimer` expires), it restores the normal state (`SPEED_50`) via `_set_normal_state`, which also calls `reset()` on all sub-components.

- **`update_cross_left_forced_decision(taxi_maneuver, aruco_id, aruco_distance_m)`**
  Starts a 2.5 s forced window for `CROSS_LEFT` when ArUco 13 is at ≤ 0.70 m.

- **`update_cross_right_forced_decision(fsm, taxi_state, aruco_id, aruco_distance_m)`**
  Delegates to `ParkingOutRightPolicy.should_start_forced`; starts a `FORCED_DURATION_S` (7.0 s) forced window for `CROSS_RIGHT`, only when no other forced window is active.

- **`update_parking_in_left_forced_decision(fsm, taxi_state, aruco_id, aruco_distance_m)`**
  Delegates to `ParkingInRightPolicy.should_start_forced`; starts a `FORCED_DURATION_S` (10.0 s) forced window for `PARKING_IN_LEFT`, only when no other forced window is active.

- **`update_parking_in_right_forced_decision(taxi_maneuver, aruco_id, aruco_distance_m)`**
  Delegates to `ParkingInPolicy.should_start_parking_in_right_forced`; starts a 6.0 s forced window for `PARKING_IN_RIGHT`.

- **`resolve_drive_state(fsm, env_state)`**
  - If a forced window is active → `current_state` is the forced state (`getattr(State, forced_state_name)`), with a fallback to `PARKING_OUT_LEFT` in case of an unexpected name mismatch.
  - Otherwise → `fsm.process(env_state, planner_return_complete=...)` decides the state normally.
  - Also returns `pid_reset_needed`, true only on forced-mode boundary transitions (entering/exiting), to avoid PID integrator windup.

- **`calculate_target_cte(current_state)`** — cascading priority:
  1. Forced CTE from the active window (`forced_cte`), if any.
  2. Fixed CTE associated with the current state's name (`maneuver_cte_by_state`), **except** for states in `_cte_only_during_forced_states` (`PARKING_OUT_LEFT`, `CROSS_LEFT`, `CROSS_RIGHT`), which only get a fixed CTE while the window is actually active.
  3. Return interpolation (`ReturningProfile`) if `current_state == State.RETURNING`.
  4. Default `0.0` (lane-centered).

- **`forced_steering_override()`** — exposes the active window's fixed steering (used in `main` to override the PID).

- **`reset()`** — resets all internal state (forced window, timer, interpolation).

---

## 10. Full mission flow (summary)

1. The car starts at `PARKING_POS`, `TaxiState = GOING_TO_PICKUP`.
2. Once ArUco 14 is close enough (`outside_decision_distance_m` = 1.30 m), it decides to exit left or right based on the `path` computed (BFS) to the pickup.
3. **If exiting left**: forced `PARKING_OUT_LEFT` maneuver (left bias, `parking_out_left.py`).
   **If exiting right**: follows the lane normally until ArUco 11, where the FSM switches to `CROSS_RIGHT`; once ArUco 11 is at ≤ 0.67 m, `ParkingOutRightPolicy` triggers the blind right turn (`parking_out_right.py`).
4. Continues the route to the pickup, crossing according to the mapped ArUcos 11/12/13.
5. Once the pickup's ArUco is reached, stops for 3.5 s (`WAITING_AT_PICKUP`).
6. Repeats the navigation process to the dropoff (`GOING_TO_DROPOFF`), stops again (`WAITING_AT_DROPOFF`).
7. Returns to parking (`RETURNING_TO_PARKING`):
   - If the route passes ArUco 11, the FSM switches to `PARKING_IN_LEFT`; once ArUco 11 is at ≤ 0.75 m, `ParkingInRightPolicy` triggers the blind left turn (`parking_in_right.py`).
   - If the route passes ArUco 12, `ParkingInPolicy` triggers `PARKING_IN_RIGHT` once it's at ≤ 0.75 m (`parking_in_left.py`).
8. Once the parking's ArUco is reached, `TaxiState = COMPLETE`, car stops.

---

## 11. Relevant constants (quick reference)

| Constant | Value | File |
|---|---|---|
| `stop_distance_m` | 0.35 m | `robotaxi_mission.py` |
| `stop_duration_s` | 3.5 s | `robotaxi_mission.py` |
| `outside_decision_distance_m` | 1.30 m | `robotaxi_mission.py` |
| `cross_left_trigger_distance_m` | 0.65 m | `robotaxi_mission.py` |
| `startup_decision_aruco_id` | 14 | `robotaxi_mission.py` |
| `parking_station_stop_distance_m` | 0.35 m | `robotaxi_mission.py` |
| `ForcedManeuverWindow.default_duration_s` | 3.5 s | `parking_out_left.py` |
| `ParkingOutTimer.duration_s` | 3.5 s (passed in by the controller) | `parking_out_left.py` |
| Forced cross-left (distance / duration) | 0.70 m / 2.5 s | `taxi_robot_cte_controller.py` |
| `PARKING_IN_RIGHT_TRIGGER_DISTANCE_M` | 0.75 m | `parking_in_left.py` |
| `PARKING_IN_RIGHT_FORCED_DURATION_S` | 6.0 s | `parking_in_left.py` |
| `TRIGGER_DISTANCE_M` (cross-right) | 0.67 m | `parking_out_right.py` |
| `FORCED_DURATION_S` (cross-right) | 7.0 s | `parking_out_right.py` |
| `FORCED_CTE` / `FORCED_STEERING` (cross-right) | 0.70 / -1.0 | `parking_out_right.py` |
| `TRIGGER_DISTANCE_M` (parking-in-left) | 0.75 m | `parking_in_right.py` |
| `FORCED_DURATION_S` (parking-in-left) | 10.0 s | `parking_in_right.py` |
| `FORCED_CTE` / `FORCED_STEERING` (parking-in-left) | -0.90 / 0.90 | `parking_in_right.py` |
| `lane_offset` (CTE controller, default) | 0.70 | `taxi_robot_cte_controller.py` |
| `return_duration_s` (CTE controller, default) | 1.5 s | `taxi_robot_cte_controller.py` |

---

## 12. Design notes

- **Separation of concerns**: `RobotaxiMission` only knows "mission" (pickup/dropoff/parking); `TaxiRobotCTEController` only knows "how to force CTE/steering during maneuvers"; each policy (`ParkingInPolicy`, `ParkingOutRightPolicy`, `ParkingInRightPolicy`) isolates the specific trigger rule for one concrete maneuver. This keeps each file small, independently testable, and tunable without touching the controller.
- **Blind maneuvers vs. lane-guided driving**: whenever the lane isn't reliable at an intersection/parking entrance, the system uses `ForcedManeuverWindow` (fixed time, hardcoded CTE/steering) instead of trusting lane detection.
- **Shared marker, decided by state**: ArUco 11 is used for two opposite maneuvers (`CROSS_RIGHT` outbound, `PARKING_IN_LEFT` inbound). The ambiguity is resolved by the mission's `TaxiState`, not by the ArUco itself — each policy also checks `taxi_state in TRIGGER_TAXI_STATES` before firing.
- **Two readings of the same ArUco**: for the ArUco-11 blind maneuvers, there's always a first, farther reading (`outside_decision_distance_m`, handled in `robotaxi_mission.py`) that only changes the FSM, and a second, closer reading (each policy's `TRIGGER_DISTANCE_M`) that actually starts the blind turn. The policies key off `fsm_state` (which persists) rather than `TaxiManeuver` (which has already gone back to `NONE`).
- **Anti-repetition**: the `aruco_armed` flag prevents the same ArUco from firing the same maneuver repeatedly while it stays in view.
- **Timeout safety**: `ParkingOutTimer` ensures a parking-exit maneuver doesn't get stuck indefinitely if the relevant ArUco is never seen again.
- **Simple, deterministic pathfinding**: `find_path` uses BFS over a static grid — sufficient since the map is fixed and small, with no need for A*-style heuristics.