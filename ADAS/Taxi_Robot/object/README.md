# Object

## Index
- [Overview](#overview)
- [Classes](#classes)
  - [CorridorChecker](#corridorchecker)
  - [build_environment_state](#build_environment_state)
  - [ObstacleTracker](#obstacletracker)
  - [perception_objects](#perception_objects)
- [Data Contract](#data-contract)
- [Debug](#debug)
- [Notes](#notes)

## Overview
Higher-level object perception module. Receives raw detections from `post_processing/obj/` and performs corridor presence evaluation, obstacle tracking, and environment state aggregation. Output feeds directly into `decision/`.

## Classes

### `CorridorChecker`
Evaluates whether a detection is inside the lane corridor using the BEV transformation.

#### `__init__(bev_transform)`
Stores the BEV transform used to map frame points to bird's-eye-view coordinates.

#### `check_and_debug(bbox, fit_result, frame_shape)`
Maps the bottom-center of the bounding box to BEV and checks if it lies between the fitted lane lines.

**Output** — `dict` with `in_corridor`, `rel_area`, `bev_x`, `bev_y`, `l_x`, `r_x`.

---

### `build_environment_state`
Standalone function that iterates raw detections, runs corridor checking, and builds a structured `EnvironmentState`.

```python
build_environment_state(detections, fit_result, checker, frame_shape) → EnvironmentState
```

| Parameter | Type | Description |
|---|---|---|
| `detections` | `list[dict]` | Raw detections from `ObjectDetector.process()` |
| `fit_result` | `LaneFitResult` | Lane fit from `SlidingWindowsLaneFitter` |
| `checker` | `CorridorChecker` | Instance used to map detections to BEV |
| `frame_shape` | `tuple` | Original frame shape `(H, W, 3)` |

**Output** — `EnvironmentState` ready to pass to `VehicleFSM.process()`.

---

### `ObstacleTracker`
Tracks the most relevant obstacle in the corridor across frames and classifies the situation.

#### `__init__(area_brake_threshold, area_avoidance_min, frames_to_confirm, frame_width_bev)`

| Parameter | Default in `main.py` | Description |
|---|---|---|
| `area_brake_threshold` | `0.060` | Area delta per frame that triggers BRAKE |
| `area_avoidance_min` | `0.010` | Minimum area to consider avoidance |
| `frames_to_confirm` | `4` | Consecutive frames to confirm avoidance |
| `frame_width_bev` | `640` | BEV image width in pixels |

#### `update(detections_in_corridor) → ObstacleInfo`
Classifies the obstacle situation as `CLEAR`, `AVOIDANCE`, or `BRAKE`.

#### `reset()`
Resets internal state. Called by `main` when leaving avoidance states.

---

### `perception_objects`
Shared data contracts used across object detection and decision-making.

#### `ClassID` (IntEnum)
| Value | Name |
|---|---|
| 0 | `SIGN_50` |
| 1 | `SIGN_80` |
| 2 | `GATE` |
| 3 | `CROSSWALK_SIGN` |
| 4 | `STOP_SIGN` |
| 5 | `YIELD_SIGN` |
| 6 | `CAR` |
| 7 | `DANGER_SIGN` |
| 8 | `OBSTACLE` |
| 9 | `LIGHT_GREEN` |
| 10 | `LIGHT_OFF` |
| 11 | `LIGHT_RED` |
| 12 | `LIGHT_YELLOW` |

#### `ObstacleSituation` (Enum)
| Value | Meaning |
|---|---|
| `CLEAR` | No relevant obstacle |
| `AVOIDANCE` | Obstacle detected in advance |
| `BRAKE` | Obstacle appeared suddenly |

#### `Detection` (dataclass)
| Field | Type | Description |
|---|---|---|
| `class_id` | `ClassID` | Detected object class |
| `in_corridor` | `bool` | Whether the object is inside the lane corridor |
| `relative_area` | `float` | Object area as a fraction of the full frame |

#### `EnvironmentState` (dataclass)
| Field | Type | Default | Description |
|---|---|---|---|
| `detections` | `List[Detection]` | — | All detections in the current frame |
| `corridor_clear` | `bool` | — | `True` if no obstacle/car in corridor |
| `lead_car_detected` | `bool` | `False` | `True` if a car is detected in corridor |
| `lead_car_area` | `float` | `0.0` | Relative area of the lead car (used by ACC) |

## Data Contract
| Field | Type | Source | Destination |
|---|---|---|---|
| `detections` | `list[dict]` | `post_processing/obj` | `CorridorChecker`, `ObstacleTracker` |
| `EnvironmentState` | `dataclass` | `build_environment_state` | `decision/VehicleFSM` |
| `ObstacleInfo` | `dataclass` | `ObstacleTracker` | `decision/VehicleFSM` |

## Debug

### Lifecycle logs
None.

### Per-frame debug
No dedicated debug flag. Corridor state is visible through FSM state transitions logged by `main`.

## Notes
- `CorridorChecker` depends on a valid `LaneFitResult`. When no lanes are found, it falls back to a fixed centre corridor (`35%–65%` of frame width).
- `ObstacleTracker` only tracks `ClassID.OBSTACLE` — cars are handled separately via `lead_car_detected` in `EnvironmentState`.
- `ObstacleTracker.reset()` must be called by `main` whenever the FSM leaves avoidance states.
