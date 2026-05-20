# Post-Processing

## Index
- [Overview](#overview)
- [Submodules](#submodules)
- [Data Contract](#data-contract)
- [Execution Flow](#execution-flow)
- [Notes](#notes)

## Overview
This layer translates raw inference outputs into domain structures used by the rest of the pipeline.

It is divided into two subdomains:
- `lane` for lane segmentation and mask cleanup
- `object` for object detection and corridor verification

## Submodules
- [Lane Post-Processing](lane/README.md)
- [Object Post-Processing](object/README.md)

## Input
| Field | Type | Meaning |
|---|---|---|
| `outputs_lane` | `dict` | Raw tensors from the lane segmentation model |
| `outputs_obj` | `dict` | Raw tensors from the object detection model |

## Output
| Field | Type | Meaning |
|---|---|---|
| `binary_mask` | `numpy.ndarray uint8` | Cleaned binary mask passed to LFA |
| `detections` | `list[dict]` | Structured detections passed to decision |

## Data Contract
| Field | Type | Meaning |
|---|---|---|
| `outputs_lane` | `dict` | Input to the `lane` submodule |
| `outputs_obj` | `dict` | Input to the `object` submodule |
| `binary_mask` | `numpy.ndarray uint8` | Output of the `lane` submodule |
| `detections` | `list[dict]` | Output of the `object` submodule |

## Execution Flow
- `outputs_lane` → `lane/YoloSegDecoder.decode_to_mask(...)`
- `binary_mask` → `lane/MaskFilters.process(...)`
- `outputs_obj` → `object/ObjectDetector.process(...)`
- `detections` → `object/CorridorChecker.check_and_debug(...)`

## Notes
- This layer sits between `inference` and the geometry/decision modules.
- Model-specific details are encapsulated in the corresponding submodules.
- `EnvironmentState` and `ObstacleTracker` are built in the `object` submodule; their outputs feed directly into `decision/`.
- The `object` submodule holds hardcoded output tensor keys (`yolo26n/conv61`, etc.) that are specific to `yolo26n_v4.hef`. Switching models requires updating `ObjectDetector.process()`.
