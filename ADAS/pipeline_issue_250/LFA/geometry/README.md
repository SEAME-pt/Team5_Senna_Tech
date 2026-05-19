# LFA Geometry

## Index
- [Overview](#overview)
- [Classes](#classes)
  - [BEVTransform](#bevtransform)
  - [SlidingWindowsLaneFitter](#slidingwindowslanefitter)
- [Data Contract](#data-contract)
- [Debug](#debug)
- [Notes](#notes)

## Overview
Processes the binary lane mask to extract geometric information useful for vehicle control. Transforms the mask to a top-down view and fits 2nd-degree polynomials to the detected lanes, producing the cross-track error used by the PID controller.

## Classes

### `BEVTransform`
Applies a perspective transform to convert the front-facing camera view into a Bird's-Eye View (top-down) image.

#### `__init__(w, h, src=None, dst=None)`
Computes the perspective transform matrix from source and destination points.

| Parameter | Default | Description |
|---|---|---|
| `w`, `h` | `640`, `360` | Frame dimensions in pixels |
| `src` | `DEFAULT_SRC` | 4 normalised source points in the original frame |
| `dst` | `DEFAULT_DST` | 4 normalised destination points in the BEV frame |

The default `src` points were calibrated on the RPi and should not be changed without re-running the calibration procedure.

#### `warp(img) → numpy.ndarray`
Applies the forward perspective transform (camera → BEV).

#### `unwarp(img) → numpy.ndarray`
Applies the inverse perspective transform (BEV → camera). Used by `lane_visualiser` to overlay lane lines back onto the original frame.

**Data contract**
| Field | Type | Shape | Meaning |
|---|---|---|---|
| Input `img` | `numpy.ndarray uint8` | `(H, W)` | Binary mask or BGR frame |
| Output | `numpy.ndarray uint8` | `(H, W)` | Warped image |

---

### `SlidingWindowsLaneFitter`
Locates the left and right lane lines in the BEV mask using a histogram + sliding windows approach and fits a 2nd-degree polynomial to each.

#### `__init__(cam_height, n_windows, margin, min_pixels, lane_width_px)`

| Parameter | Default | Description |
|---|---|---|
| `cam_height` | `360` | Frame height in pixels |
| `n_windows` | `12` | Number of sliding windows per lane |
| `margin` | `40` | Half-width of each window in pixels |
| `min_pixels` | `20` | Minimum pixels in a window to recenter it |
| `lane_width_px` | `180.0` | Expected lane width in BEV pixels (calibrated) |

#### `fit(bev_mask) → LaneFitResult`
Main entry point. Runs the full detection pipeline on a BEV binary mask.

**Behavior**
1. Computes a histogram of the lower half of the mask to find lane base positions.
2. Slides windows upward on each side, collecting lane pixels.
3. Fits a 2nd-degree polynomial `x = a·y² + b·y + c` to each set of pixels.
4. If one lane is not found, estimates it from the other using `lane_width_px`.
5. Computes CTE from the midpoint between the two fitted lanes.

**Output** — `LaneFitResult` (see `core/README.md`).

#### Sanity check on lane width
The fitter validates that the detected lane width is within `50%–150%` of the tracked `lane_width_px`. Detections outside this range are rejected to avoid spurious fits from noise.

## Data Contract
| Field | Type | Shape | Meaning |
|---|---|---|---|
| `binary_mask` | `numpy.ndarray uint8` | `(H, W)` | Filtered lane mask from `post_processing/lane` |
| `bev_mask` | `numpy.ndarray uint8` | `(H, W)` | BEV-transformed mask |
| `fit_result` | `LaneFitResult` | — | Polynomials, CTE, and debug image |

## Debug
Neither class exposes a `debug` flag. Visual debug is available via `LaneFitResult.debug_image`, which contains the sliding windows drawn on the BEV mask when lanes are detected.

## Notes
- `DEFAULT_SRC` calibration points were validated on the RPi — the commented-out values above them represent previous attempts kept for reference.
- `lane_width_px=180.0` was tuned empirically. If the track changes, this value may need adjustment.
- CTE is normalised to `[-1.0, 1.0]` relative to half the lane width.
- If neither lane is found, `fit_result.cte_norm` is `None` — `main` should fall back to `0.0`.
