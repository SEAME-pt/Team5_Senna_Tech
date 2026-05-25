# Decision Module

## Index
- [Overview](#overview)
- [Classes](#classes)
  - [VehicleFSM](#vehiclefsm)
  - [PathPlanner](#pathplanner)
  - [AdaptiveCruiseControl](#adaptivecruisecontrol)
  - [PID](#pid)
- [Constants](#constants)
  - [STATE_THROTTLE](#state_throttle)
- [Data Contract](#data-contract)
- [Debug](#debug)
- [Notes](#notes)

## Overview
Coordinates the high-level behaviour of the vehicle. Receives the environment state from perception, decides the current driving mode via a state machine, computes the target cross-track error via the path planner, and outputs a steering angle via the PID controller.

## Classes

### `VehicleFSM`
Finite state machine that maps the perceived environment to a driving state.

#### States
| State | Value | Description |
|---|---|---|
| `SPEED_50` | 8 | Normal speed — 50 zone |
| `SPEED_80` | 10 | Fast speed — 80 zone |
| `SPEED_SLOW` | 5 | Reduced speed — crosswalk or yellow light |
| `FOLLOW` | 4 | Adaptive cruise — following a lead car |
| `STOP` | 0 | Full stop — red light or stop sign |
| `EMERGENCY` | 200 | Emergency brake — obstacle too close |
| `PREPARE_AVOID` | 11 | Avoidance phase 1 — begin lateral offset |
| `AVOIDING` | 12 | Avoidance phase 2 — obstacle still visible |
| `BLIND_WAIT` | 13 | Avoidance phase 3 — obstacle lost, waiting |
| `RETURNING` | 14 | Avoidance phase 4 — interpolating back to centre |

#### `__init__()`
Initialises all confirmation buffers, the initial state (`SPEED_50`), and avoidance tracking variables.

#### `process(env, obstacle_situation, planner_return_complete) → State`
Main entry point called once per frame. Evaluates environment conditions and transitions the FSM.

**Inputs**
- `env`: `EnvironmentState` from object post-processing.
- `obstacle_situation`: `ObstacleSituation` from `ObstacleTracker`.
- `planner_return_complete`: `bool` from `PathPlanner.return_complete()`.

**Output** — current `State`.

#### `signal_blind_wait_timeout()`
Called by `main` when the blind wait timer expires. Transitions `BLIND_WAIT → RETURNING`.

#### `_evaluate_environment(env) → dict`
Scans detections and returns a conditions dictionary used for state transitions.

#### `_handle_avoidance_sequence(env, obstacle_situation, planner_return_complete) → State`
Manages the 4 avoidance phases. Only called when the FSM is in `AVOIDANCE_STATES`.

#### `_transition(new_state, reason)`
Performs the state change and logs the transition.

#### `_reset_buffers()`
Resets all confirmation buffers after a state transition.

#### `ConfirmationBuffer`
Helper class that requires N consecutive frames of a condition before confirming it, preventing noise-triggered transitions.

#### `Thresholds`
| Constant | Value | Meaning |
|---|---|---|
| `AREA_EMERGENCY` | `0.05` | Obstacle area triggering emergency brake |
| `AREA_AVOIDANCE` | `0.015` | Obstacle area triggering avoidance |
| `AREA_SIGN` | `0.004` | Minimum area for traffic signs |
| `AREA_TRAFFIC_LIGHT` | `0.004` | Minimum area for traffic lights |
| `AREA_FOLLOW_ENTER` | `0.022` | Lead car area to enter FOLLOW |
| `AREA_FOLLOW_EXIT` | `0.017` | Lead car area to exit FOLLOW (hysteresis) |

---

### `PathPlanner`
Computes the target CTE to pass to the PID based on the current FSM state.

#### `__init__(lane_offset, blind_wait_time, return_duration_s)`
| Parameter | Default | Description |
|---|---|---|
| `lane_offset` | `0.38` (class default); `0.80` in `main.py` | Normalised lateral offset during avoidance |
| `blind_wait_time` | `2.5` | Seconds to wait in `BLIND_WAIT` before returning |
| `return_duration_s` | `1.5` | Duration of the return-to-centre interpolation |

#### `calculate_target_cte(current_state, obstacle_side) → float`
Returns the target CTE for the current frame.

- `PREPARE_AVOID` / `AVOIDING` / `BLIND_WAIT` → shifted CTE (opposite side of obstacle)
- `RETURNING` → linearly interpolates from shifted CTE → `0.0`
- All other states → `0.0` (lane centre)

#### `check_blind_wait_timeout() → bool`
Starts the timer on first call. Returns `True` when `blind_wait_time` seconds have elapsed.

#### `reset_blind_timer()`
Resets the blind wait timer. Called by `main` when the FSM leaves `BLIND_WAIT`.

#### `return_complete() → bool`
Returns `True` when the return interpolation has finished.

---

### `AdaptiveCruiseControl`
Computes throttle when following a lead car, scaling linearly with the car's relative area.

#### `__init__()`
| Attribute | Value | Description |
|---|---|---|
| `stop_area` | `0.05` | Area at which the car is too close — throttle = 0 |
| `follow_area` | `0.02` | Minimum area to start following |
| `max_throttle` | `8` | Maximum throttle in follow mode |

#### `compute_follow_error(lead_car_area) → int`
Returns throttle `[0, max_throttle]` based on the lead car's relative area. Returns `0` if area exceeds `stop_area`.

---

### `PID`
Proportional-Integral-Derivative controller for steering.

#### `__init__(kp, ki, kd)`
| Parameter | Tuned value | Description |
|---|---|---|
| `kp` | `1.3` | Proportional gain |
| `ki` | `0.1` | Integral gain |
| `kd` | `0.1` | Derivative gain |

#### `update(target, current, dt) → float`
Computes PID output given target CTE, actual CTE, and elapsed time.

**Output** — steering angle clamped to `[-1.0, 1.0]`.

#### `reset()`
Clears integral accumulator and previous error.

#### `set_integral_limit(limit)` / `set_output_limit(limit)`
Runtime adjustment of anti-windup and output saturation limits.

## Constants

### `STATE_THROTTLE`
Maps each FSM `State` to its default throttle value. Defined alongside `State` in `decision_fsm.py`.

| State | Throttle | Description |
|---|---|---|
| `EMERGENCY` | `200` | Abstract value — triggers emergency brake on MCU |
| `STOP` | `0` | Full stop |
| `SPEED_SLOW` | `5` | Reduced speed |
| `SPEED_50` | `8` | Normal speed |
| `SPEED_80` | `10` | Fast speed |
| `FOLLOW` | `0` | Overridden by `AdaptiveCruiseControl` |
| `PREPARE_AVOID` | `5` | Slow during avoidance preparation |
| `AVOIDING` | `5` | Slow during active avoidance |
| `BLIND_WAIT` | `5` | Slow during blind wait |
| `RETURNING` | `5` | Slow during return to centre |

## Data Contract
| Field | Type | Source | Destination |
|---|---|---|---|
| `EnvironmentState` | dataclass | `post_processing/object` | `VehicleFSM.process()` |
| `ObstacleSituation` | enum | `ObstacleTracker.update()` | `VehicleFSM.process()` |
| `State` | enum | `VehicleFSM.process()` | `PathPlanner`, `main` |
| `target_cte` | `float` | `PathPlanner.calculate_target_cte()` | `PID.update()` |
| `steering` | `float [-1, 1]` | `PID.update()` | `CanSender` |
| `throttle` | `int` | `STATE_THROTTLE` / `AdaptiveCruiseControl` | `CanSender` |

## Debug

### Lifecycle logs (always active)
| Event | Level | Message |
|---|---|---|
| FSM state transition | `INFO` | `FSM Transition: OLD_STATE -> NEW_STATE [reason]` |

### Per-frame logs
None — this module does not emit per-frame logs. State transitions are logged only when they occur.

### How to enable
```python
logging.getLogger("FSM").setLevel(logging.INFO)
```

## Notes
- The FSM starts in `SPEED_50` — the vehicle moves immediately on boot.
- `AVOIDANCE_STATES` are handled in isolation: traffic signs and area thresholds are ignored during a maneuver.
- `STOP_SIGN` has a cooldown (`STOP_SIGN_COOLDOWN = 5s`) to prevent re-triggering on the same sign.
- `PathPlanner` uses `time.perf_counter()` for return interpolation (frame-rate independent) and `time.time()` for the blind wait timer.
- `AdaptiveCruiseControl` is only active in `FOLLOW` state — throttle is otherwise determined by `STATE_THROTTLE`.
- `STATE_THROTTLE` is defined in `decision_fsm.py` alongside `State` — it maps each FSM state to its default throttle value and is imported directly from `decision`.
