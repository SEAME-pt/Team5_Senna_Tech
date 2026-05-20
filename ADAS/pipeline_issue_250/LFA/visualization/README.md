# LFA Visualization

## Index
- [Overview](#overview)
- [Functions](#functions)
  - [draw_lane_overlay](#draw_lane_overlay)
  - [draw_text_overlay](#draw_text_overlay)
- [Data Contract](#data-contract)
- [Debug](#debug)
- [Notes](#notes)

## Overview
Renders lane detection results onto the original camera frame for visual debugging and display. Unwarps the BEV overlays back to the camera perspective before blending with the original image.

## Functions

### `draw_lane_overlay(frame_rgb, fit_result, bev) → numpy.ndarray`
Draws the detected lane lines and corridor fill onto the original camera frame.

**Behavior**
1. Computes polynomial points for each y-value in the frame.
2. If both lanes are found, fills the corridor between them with semi-transparent green.
3. Draws a cyan centre line between the two lanes.
4. Draws each lane line — red for real left lane, blue for real right lane, cyan for virtual (estimated) lanes.
5. Unwarps the overlay from BEV back to camera perspective using `bev.unwarp()`.
6. Blends the overlay with the original frame (`alpha=0.4`).
7. Draws the BEV source trapezoid for calibration reference.

**Inputs**
| Field | Type | Description |
|---|---|---|
| `frame_rgb` | `numpy.ndarray` | Original **RGB** camera frame |
| `fit_result` | `LaneFitResult` or `TrackedLaneFit` | Lane polynomials |
| `bev` | `BEVTransform` | Used to unwarp overlays back to camera view |

**Output** — annotated **RGB** frame.

#### Visual legend
| Element | Color | Meaning |
|---|---|---|
| Lane fill | Semi-transparent green | Detected drivable corridor |
| Centre line | Cyan | Midpoint between lanes |
| Left lane | Blue `(0,0,255)` in RGB | Directly detected |
| Right lane | Red `(255,0,0)` in RGB | Directly detected |
| Virtual lane (either side) | Cyan `(0,255,255)` in RGB | Estimated from the other lane |
| BEV trapezoid | Magenta | Calibration reference points |

---

### `draw_text_overlay(frame, fit_result, fps=None, inf_ms=None) → numpy.ndarray`
Draws timing and performance metrics onto the frame. Currently only renders the FPS and inference time label.

**Inputs**
| Field | Type | Description |
|---|---|---|
| `frame` | `numpy.ndarray` | BGR frame (modified in-place) |
| `fit_result` | `LaneFitResult` | Used for CTE and curvature (currently commented out) |
| `fps` | `float` or `None` | Pipeline FPS to display |
| `inf_ms` | `float` or `None` | Hailo inference time in ms |

**Output** — annotated frame.

## Data Contract
| Field | Type | Meaning |
|---|---|---|
| `fit_result` | `LaneFitResult` | Source of lane polynomials for rendering |
| `bev` | `BEVTransform` | Provides `unwarp()` and `DEFAULT_SRC` for overlay |
| Output frame | `numpy.ndarray RGB` | Frame with lane overlays blended in |

## Debug
No `debug` flag — visualisation is itself the debug output. Call `draw_lane_overlay()` to inspect what the geometry stage detected.

## Notes
- `draw_lane_overlay` returns early (no overlay) if both `left_fit` and `right_fit` are `None`.
- The BEV trapezoid overlay uses `bev.DEFAULT_SRC` — it will only appear correctly if the default calibration points are active.
- `draw_text_overlay` has CTE and curvature rendering commented out — these were used during development and can be re-enabled for debugging.
