# Object Post-Processing (obj)

## Index
- [Overview](#overview)
- [Classes](#classes)
  - [ObjectDetector](#objectdetector)
- [Data Contract](#data-contract)
- [Debug](#debug)
- [Notes](#notes)

## Overview
Decodes raw object detection model outputs into structured bounding boxes with class scores. Applies NMS and rescales boxes to the original frame dimensions. Output is passed to the top-level `object/` module for corridor checking and tracking.

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

#### `process(outputs, frame_shape)`
Decodes all 3 scale heads and returns a list of structured detections rescaled to the original frame.

**Output** — `list[dict]` with `bbox`, `score`, `class_id`, `class_name`.

#### `draw(frame, detections)`
Draws bounding boxes and labels onto the frame. Color is red for in-corridor detections, dark green otherwise.

**Output** — annotated frame (RGB).

## Data Contract
| Field | Type | Meaning |
|---|---|---|
| `outputs_obj` | `dict` | Raw tensors from the object detection model |
| `detections` | `list[dict]` | Decoded bounding boxes passed to `object/` |

## Debug

### Lifecycle logs
None.

### Per-frame debug
Visual debug via `draw()` — renders bounding boxes and relative areas on the frame.

| Visual cue | Meaning |
|---|---|
| Red box | Detection inside the lane corridor |
| Dark green box | Detection outside the corridor |
| `A: X.X%` label | Relative area of the bounding box |
| Magenta dot | Bottom-center of the bounding box (BEV reference point) |

## Notes
- Expects the exact tensor keys from `yolo26n_v4.hef` (`yolo26n/conv61`, etc.) — changing the model requires updating `ObjectDetector.process()`.
- Corridor checking, obstacle tracking, and perception data types live in the top-level `object/` module.
