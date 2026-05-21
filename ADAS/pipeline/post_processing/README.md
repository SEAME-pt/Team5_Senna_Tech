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
- `obj` for raw object detection decoding

## Submodules
- [Lane Post-Processing](lane/README.md)
- [Object Post-Processing](obj/README.md)

## Input
| Field | Type | Meaning |
|---|---|---|
| `outputs_lane` | `dict` | Raw tensors from the lane segmentation model |
| `outputs_obj` | `dict` | Raw tensors from the object detection model |

## Output
| Field | Type | Meaning |
|---|---|---|
| `binary_mask` | `numpy.ndarray uint8` | Cleaned binary mask passed to LFA |
| `detections` | `list[dict]` | Raw structured detections passed to `object/` |

## Data Contract
| Field | Type | Meaning |
|---|---|---|
| `outputs_lane` | `dict` | Input to the `lane` submodule |
| `outputs_obj` | `dict` | Input to the `obj` submodule |
| `binary_mask` | `numpy.ndarray uint8` | Output of the `lane` submodule |
| `detections` | `list[dict]` | Output of the `obj` submodule |

## Execution Flow
- `outputs_lane` → `lane/YoloSegDecoder.decode_to_mask(...)`
- `binary_mask` → `lane/MaskFilters.process(...)`
- `outputs_obj` → `obj/ObjectDetector.process(...)`

## Notes
- This layer sits between `inference` and the geometry/decision modules.
- Model-specific details are encapsulated in the corresponding submodules.
- Corridor checking, obstacle tracking, and perception objects are handled by the top-level `object/` module.
- The `obj` submodule holds hardcoded output tensor keys (`yolo26n/conv61`, etc.) that are specific to `yolo26n_v4.hef`. Switching models requires updating `ObjectDetector.process()`.
