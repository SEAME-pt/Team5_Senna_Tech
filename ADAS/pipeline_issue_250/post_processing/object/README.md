# Object Post-Processing

## Index
- [Overview](#overview)
- [Classes](#classes)
- [Data Contract](#data-contract)
- [Notes](#notes)

## Overview
Processes raw object detection model outputs, generates bounding boxes, and classifies each detection for use in decision-making.

## Classes

### `ObjectDetector`
Responsible for decoding object model tensors, applying NMS, and drawing detections.

#### `__init__()`
Initializes class names, confidence thresholds, and NMS settings.

**Effects**
- Defines the list of supported classes.
- Defines the thresholds used in decoding and box suppression.

#### `sigmoid(x)`
Applies the sigmoid function to class logits.

#### `make_grid(h, w)`
Creates the spatial grid used to transform offsets into absolute coordinates.

#### `decode_output(bbox, cls, stride)`
Converts a network header into boxes, scores, and classes already filtered by confidence.

**Behavior**
- Applies sigmoid to classes.
- Constructs the spatial grid.
- Converts offsets into bounding boxes in image space.
- Filters by confidence.

**Output**
- Filtered `boxes`, `scores`, and `classes`.

#### `nms(boxes, scores)`
Applies Non-Maximum Suppression to remove overlapping boxes.

**Behavior**
- Reads tensors by model scale.
- Converts offsets and classes into bounding boxes in image space.
- Filters by confidence.
- Applies NMS to eliminate overlapping detections.
- Rescales boxes to the original frame size.

**Output**
- Indices of the kept boxes.

#### `process(outputs, frame_shape)`
Decodes raw inference tensors and returns a list of structured detections.

**Inputs**
- `outputs`: raw inference tensors from the object model.
- `frame_shape`: original frame shape used for rescaling.

**Output**
- List of dictionaries with `bbox`, `score`, `class_id`, and `class_name`.

#### `draw(frame, detections)`
Draws bounding boxes and labels onto the frame.

**Behavior**
- Iterates through each structured detection.
- Chooses color and thickness based on `in_corridor`.
- Draws rectangles, labels, and visual reference points.

**Input**
- `frame`: BGR image where overlays will be drawn.
- `detections`: list of detections produced by `process`.

**Output**
- Frame annotated with boxes and labels.

### `CorridorChecker`
Responsible for evaluating if a detection is within the lane corridor using the BEV transformation.

#### `__init__(bev_transform)`
Stores the BEV transform used to map frame points to lane coordinates.

**Effects**
- Maintains a reference to the transformation object that exposes the `M` matrix.

#### `map_point_to_bev(x, y)`
Converts a point from the original frame to BEV coordinates.

**Output**
- Point transformed into BEV.

#### `check_and_debug(bbox, fit_result, frame_shape)`
Determines if the detection is within the lane corridor and generates debug data.

**Behavior**
- Maps the bottom-center of the bbox to BEV coordinates.
- Calculates the relative area of the object in the image.
- Compares the detection position with the estimated corridor lines.
- Returns a dictionary with corridor presence flags and debug values.

**Inputs**
- `bbox`: detection bounding box.
- `fit_result`: lane fit result.
- `frame_shape`: original frame shape.

**Output**
- `dict` with `in_corridor`, `rel_area`, and auxiliary debug metrics.

## Data Contract
| Field | Type | Meaning |
|---|---|---|
| `outputs_obj` | `dict` | Raw tensors from the object detection model |
| `detections` | `list[dict]` | List of bounding boxes, scores, and classes |
| `EnvironmentState` | `dataclass` | Aggregated state for decision-making |

## Notes
- This layer prepares detections for `decision` and corridor verification.
