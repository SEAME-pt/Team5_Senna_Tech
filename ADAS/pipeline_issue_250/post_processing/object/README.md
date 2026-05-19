# Object Post-Processing

## Index
- [Overview](#overview)
- [Classes](#classes)
  - [ObjectDetector](#objectdetector)
  - [CorridorChecker](#corridorchecker)
  - [build_environment_state](#build_environment_state)
  - [ObstacleTracker](#obstacletracker)
  - [perception_objects](#perception_objects)
- [Data Contract](#data-contract)
- [Debug](#debug)
- [Notes](#notes)

## Overview
Processes raw object detection model outputs, generates bounding boxes, classifies each detection, evaluates corridor presence, and tracks obstacle evolution across frames for use in decision-making.

## Classes

### `ObjectDetector`
Decodes raw object detection tensors, applies NMS, and draws detections on frames.

#### `__init__()`
Initializes class names, confidence thresholds, and NMS settings.

| Attribute | Value | Description |
|---|---|---|
| `class_names` | 13 classes | Ordered list matching model output indices |
| `conf_thresh` | `0.25` | Minimum score to keep a detection |
| `nms_thresh` | `0.45` | IoU threshold for NMS suppression |
| `num_classes` | `13` | Number of output classes |

#### `sigmoid(x)`
Applies the sigmoid function to class logits.

#### `make_grid(h, w)`
Creates the spatial grid used to transform offsets into absolute coordinates.

#### `decode_output(bbox, cls, stride)`
Converts a network scale head into boxes, scores, and classes filtered by confidence.

**Output** — filtered `boxes`, `scores`, `classes`.

#### `nms(boxes, scores)`
Applies Non-Maximum Suppression to remove overlapping boxes.

**Output** — indices of kept boxes.

#### `process(outputs, frame_shape)`
Decodes all 3 scale heads and returns a list of structured detections rescaled to the original frame.

**Output** — `list[dict]` with `bbox`, `score`, `class_id`, `class_name`.

#### `draw(frame, detections)`
Draws bounding boxes and labels onto the frame. Color is red for in-corridor detections, dark green otherwise.

**Output** — annotated frame.

---

### `CorridorChecker`
Evaluates whether a detection is inside the lane corridor using the BEV transformation.

#### `__init__(bev_transform)`
Stores the BEV transform used to map frame points to bird's-eye-view coordinates.

#### `map_point_to_bev(x, y)`
Converts a point from the original frame to BEV coordinates using `cv2.perspectiveTransform`.

**Output** — `(bev_x, bev_y)` in BEV pixel coordinates.

#### `check_and_debug(bbox, fit_result, frame_shape)`
Maps the bottom-center of the bounding box to BEV, computes relative area, and checks if the point lies between the fitted lane lines.

**Inputs**
- `bbox`: `(x1, y1, x2, y2)` bounding box.
- `fit_result`: `LaneFitResult` from `LFA`.
- `frame_shape`: original frame shape for area calculation.

**Output** — `dict` with `in_corridor`, `rel_area`, `bev_x`, `bev_y`, `l_x`, `r_x`.

---

### `build_environment_state`
Standalone function that iterates raw detections, runs corridor checking on each, and builds a structured `EnvironmentState` ready for the FSM.

```python
build_environment_state(detections, fit_result, checker, frame_shape) → EnvironmentState
```

**Inputs**
| Parameter | Type | Description |
|---|---|---|
| `detections` | `list[dict]` | Raw detections from `ObjectDetector.process()` |
| `fit_result` | `LaneFitResult` | Lane fit from `SlidingWindowsLaneFitter` |
| `checker` | `CorridorChecker` | Instance used to map detections to BEV |
| `frame_shape` | `tuple` | Original frame shape `(H, W, 3)` |

**Behavior**
- Calls `checker.check_and_debug()` for each detection.
- Populates `in_corridor`, `relative_area`, and `debug_info` back into each `det_dict`.
- Builds `Detection` objects and appends them to `EnvironmentState.detections`.
- Sets `corridor_clear`, `lead_car_detected`, and `lead_car_area` based on corridor presence.

**Output** — `EnvironmentState` ready to pass to `VehicleFSM.process()`.

---

### `ObstacleTracker`
Tracks the most relevant obstacle in the corridor across frames. Classifies the situation based on area growth rate and persistence.

#### `__init__(area_brake_threshold, area_avoidance_min, frames_to_confirm, frame_width_bev)`

| Parameter | Default | Description |
|---|---|---|
| `area_brake_threshold` | `0.025` | Delta area per frame that triggers BRAKE |
| `area_avoidance_min` | `0.010` | Minimum area to consider avoidance |
| `frames_to_confirm` | `4` | Consecutive frames needed to confirm avoidance |
| `frame_width_bev` | `640` | BEV image width in pixels |

#### `update(detections_in_corridor) → ObstacleInfo`
Selects the largest obstacle in the corridor, computes area delta and BEV position, and classifies the situation.

**Situations:**
- `CLEAR` — no obstacle in corridor
- `AVOIDANCE` — obstacle present for enough frames with sufficient area
- `BRAKE` — sudden large area growth in a single frame

**Output** — `ObstacleInfo` dataclass.

#### `reset()`
Resets internal state (area and frame counter). Called by `main` when leaving avoidance states.

---

### `perception_objects`
Shared data contracts used across object detection, corridor checking, and decision-making.

#### `ClassID` (IntEnum)
Maps model output indices to semantic class names.

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
| Field | Type | Meaning |
|---|---|---|
| `outputs_obj` | `dict` | Raw tensors from the object detection model |
| `detections` | `list[dict]` | Bounding boxes, scores, and classes per frame |
| `EnvironmentState` | `dataclass` | Aggregated world state passed to `decision` |
| `ObstacleInfo` | `dataclass` | Obstacle tracking result passed to FSM |

## Debug

### Lifecycle logs
None — this module does not emit lifecycle logs.

### Per-frame debug (`ObjectDetector`)
The `ObjectDetector` does not currently expose a `debug` flag. Visual debug is done via `draw()`, which renders bounding boxes and relative areas directly on the frame.

| Visual cue | Meaning |
|---|---|
| Red box | Detection inside the lane corridor |
| Dark green box | Detection outside the corridor |
| `A: X.X%` label | Relative area of the bounding box |
| Magenta dot | Bottom-center of the bounding box (BEV reference point) |

## Notes
- `ObjectDetector.process()` expects the exact tensor keys from `yolo26n_v4.hef` (`yolo26n/conv61`, etc.) — changing the model requires updating these keys.
- `CorridorChecker` depends on a valid `LaneFitResult`. When no lanes are found, it falls back to a fixed centre corridor (`35%–65%` of frame width).
- `ObstacleTracker` only tracks `ClassID.OBSTACLE` — cars are handled separately via `lead_car_detected` in `EnvironmentState`.
- `ObstacleTracker.reset()` must be called by `main` whenever the FSM leaves avoidance states.
