# Lane Following Assistance (LFA)

This document describes the Lane Following Assistance pipeline, the subsystem responsible for detecting road lane markings, computing the vehicle's lateral deviation, and providing a steering error signal to the PID controller.

---

## Table of Contents

- [Overview](#overview)
- [Architecture](#architecture)
- [Module Breakdown](#module-breakdown)
  - [1. BEV Transform](#1-bev-transform-bev_transformpy)
  - [2. Sliding Windows Lane Fitter](#2-sliding-windows-lane-fitter-sliding_windowspy)
  - [3. Lane Visualiser](#3-lane-visualiser-lane_visualiserpy)
- [Pipeline Step by Step](#pipeline-step-by-step)
- [LaneFitResult Fields](#lanefitresult-fields)
- [Cross-Track Error (CTE)](#cross-track-error-cte)
- [Tunable Parameters](#tunable-parameters)

---

## Overview

The LFA system transforms the raw camera frame into a top-down Bird's-Eye View (BEV), detects left and right lane polynomials using a sliding window algorithm, and computes a normalized Cross-Track Error (CTE) that represents how far the vehicle is from the lane center. This CTE is passed to the PID controller, which converts it into a steering angle command sent over CAN.

---

## Architecture

```
Camera Frame (BGR)
       │
       ▼
┌──────────────────┐
│  Lane Model (NPU)│  ← YOLO segmentation on Hailo-8
└────────┬─────────┘
         │ raw segmentation outputs
         ▼
┌──────────────────┐
│  YoloSegDecoder  │  ← decodes to binary lane mask
└────────┬─────────┘
         │ binary mask (H × W, uint8)
         ▼
┌──────────────────┐
│   MaskFilters    │  ← noise removal / morphological cleaning
└────────┬─────────┘
         │ clean binary mask
         ▼
┌──────────────────┐
│  BEVTransform    │  ← perspective warp → top-down view
└────────┬─────────┘
         │ BEV binary mask
         ▼
┌──────────────────────────┐
│ SlidingWindowsLaneFitter │  ← histogram + sliding windows + polyfit
└────────┬─────────────────┘
         │ LaneFitResult
         ├─── left_fit, right_fit  (polynomial coefficients)
         ├─── cte_norm             (normalized lateral error)
         └─── curvature_px        (radius of curvature)
         ▼
┌──────────────────┐
│       main       │  ← PID Controller → steering angle → CAN Bus
└──────────────────┘
     
```

---

## Module Breakdown

### 1. BEV Transform (`bev_transform.py`)

Converts the perspective camera image into a top-down Bird's-Eye View using a homography matrix computed with `cv2.getPerspectiveTransform`.

**How it works:**

Four source points (`DEFAULT_SRC`) define the road trapezoid in the original camera image (normalized coordinates). Four destination points (`DEFAULT_DST`) define where those corners map to in the BEV output (also normalized). The resulting matrix `M` warps the image; `M_inv` reverses it for visualization.

**Default calibration points (normalized):**

| | Source (camera) | Destination (BEV) |
|---|---|---|
| Top-left | (0.10, 0.53) | (0.25, 0.00) |
| Top-right | (0.92, 0.53) | (0.75, 0.00) |
| Bottom-right | (1.31, 0.76) | (0.75, 1.00) |
| Bottom-left | (-0.29, 0.76) | (0.25, 1.00) |

> **Note:** Source points intentionally extend beyond [0,1] to capture the full road width of the trapezoidal field of view.

**Methods:**

| Method | Description |
|---|---|
| `warp(img)` | Camera → BEV (forward transform) |
| `unwarp(img)` | BEV → Camera (inverse transform, used for overlay) |

---

### 2. Sliding Windows Lane Fitter (`sliding_windows.py`)

The core of the LFA system. Given a binary BEV mask, it locates lane pixels using a sliding window search and fits a 2nd-degree polynomial to each lane.

#### Full pipeline inside `fit()`

**Step 1 — Histogram Peaks**

Sums pixel columns in the lower half of the BEV image to build a 1D histogram. The peaks on each side of center indicate the base position of the left and right lanes.

If previous detections exist (anchors from the prior frame), the histogram search is restricted to a window around the expected position, improving robustness on curves and reducing false positives.

**Step 2 — Sliding Windows**

Travels from the bottom of the image upward through `n_windows` horizontal bands. In each band:

1. A search window of width `2 × margin` is placed around the current left/right x-positions.
2. All non-zero pixels within the window are collected.
3. If the window contains at least `min_pixels` pixels, the center is recalculated as the mean x-position, and the window shifts horizontally for the next band.
4. A minimum distance constraint prevents left and right windows from crossing.

**Step 3 — Polynomial Fit**

Uses `np.polyfit` to fit a 2nd-degree polynomial `x = a·y² + b·y + c` (y as independent variable, since lanes are more vertical than horizontal).

Quality filters reject fits where:
- Fewer than 80 pixels were found
- Pixels cover less than 35% of image height
- Curvature coefficient `|a| > 0.008` (physically impossible curve)

**Step 4 — Cross-Validation**

When both lanes are detected, the pair is validated together:

| Check | Condition that triggers rejection |
|---|---|
| Bad width | Actual width deviates more than ±40% from calibrated width |
| Crossed lanes | Left x > Right x − 10 px |
| Opposite curves | Both `a` coefficients have opposite signs with `|a| > 0.001` |
| Low pixel count | Either lane has fewer than 40 pixels |

When a pair fails validation, the **less reliable fit** (fewest pixels) is discarded rather than both, preserving partial information.

**Step 5 — Virtual Lane Generation**

If only one lane is detected, the other is reconstructed by offsetting the known lane by the calibrated lane width (`tracked_lane_width_px`):

```
# Only right lane detected → mirror left
left_fit = right_fit.copy()
left_fit[2] -= tracked_lane_width_px

# Only left lane detected → mirror right
right_fit = left_fit.copy()
right_fit[2] += tracked_lane_width_px
```

Virtual lanes are flagged (`left_is_virtual` / `right_is_virtual`) and rendered in a different color in the visualizer.

**Step 6 — Adaptive Width Calibration**

When both real lanes are detected on a straight road section, the measured width updates a running EMA of `tracked_lane_width_px`:

```
tracked_lane_width_px = 0.95 × previous + 0.05 × current_width
```

This allows the system to adapt to gradual changes in camera perspective or road geometry.

**Step 7 — EMA Smoothing**

Polynomial coefficients are smoothed across frames using an Exponential Moving Average with `α = 0.8`:

```
smoothed = 0.8 × current_fit + 0.2 × previous_fit
```

This reduces jitter in the lane curves without introducing significant lag.

---

### 3. Lane Visualiser (`lane_visualiser.py`)

Renders the detected lanes back onto the original camera frame for debugging and display.

**`draw_lane_overlay(frame_bgr, fit_result, bev)`**

1. Evaluates the left and right polynomial points for every y-row in the image.
2. If both lanes exist, fills the corridor between them with a semi-transparent green polygon.
3. Draws the lane center line in cyan.
4. Draws each lane boundary:
   - Real lane → **blue** (left) / **red** (right)
   - Virtual lane → **cyan** (both sides)
5. Unwarps the overlay from BEV back to camera perspective using `bev.unwarp()`.
6. Blends the overlay onto the original frame with `cv2.addWeighted` at 40% opacity.
7. Optionally draws the BEV source trapezoid outline in magenta.

---

## Pipeline Step by Step

```
1.  Camera frame (YUV420) → converted to BGR

2.  Lane model inference (NPU) → raw segmentation outputs

3.  YoloSegDecoder → binary mask (lane = white, background = black)

4.  MaskFilters → morphological cleaning (noise removal)

5.  BEVTransform.warp() → top-down binary mask

6.  SlidingWindowsLaneFitter.fit():
    a. _histogram_peaks()     → left_base, right_base
    b. _sliding_windows()     → left_pixels, right_pixels
    c. _polyfit()             → left_fit, right_fit (or None)
    d. Cross-validation       → discard unreliable fit if pair is invalid
    e. Virtual lane           → reconstruct missing lane from width offset
    f. Width calibration      → update tracked_lane_width_px (straight only)
    g. _smooth()              → EMA on coefficients
    h. _calculate_cte()       → cte_pixels, cte_norm (with EMA + dead zone)
    i. _calculate_curvature() → curvature_px

7.  LaneFitResult returned → consumed by PathPlanner and Visualizer

8.  PathPlanner.calculate_target_cte() → target CTE (may be offset for avoidance)

9.  PID.update(target_cte, actual_cte, dt) → steering output

10. CAN Bus → steering angle sent to vehicle
```

---

## LaneFitResult Fields

| Field | Type | Description |
|---|---|---|
| `left_fit` | `np.ndarray \| None` | Polynomial coefficients `[a, b, c]` for the left lane |
| `right_fit` | `np.ndarray \| None` | Polynomial coefficients `[a, b, c]` for the right lane |
| `cte_pixels` | `float \| None` | CTE in pixels (positive = vehicle right of center) |
| `cte_norm` | `float \| None` | CTE normalized to `[-1.0, +1.0]` (fed to PID) |
| `curvature_px` | `float` | Radius of curvature in pixels (>10000 = straight) |
| `left_found` | `bool` | True if left lane was directly detected (not virtual) |
| `right_found` | `bool` | True if right lane was directly detected (not virtual) |
| `left_is_virtual` | `bool` | True if left lane was mirrored from right |
| `right_is_virtual` | `bool` | True if right lane was mirrored from left |
| `debug_image` | `np.ndarray \| None` | BEV image with window rectangles drawn (if `draw_debug=True`) |

---

## Cross-Track Error (CTE)

The CTE is the primary signal driving the PID controller. It represents the lateral displacement of the vehicle from the lane center.

**Calculation:**

```
y_eval     = image_height × 0.60          # evaluation depth (60% down from top)
left_x     = a_L·y² + b_L·y + c_L        # left lane x at y_eval
right_x    = a_R·y² + b_R·y + c_R        # right lane x at y_eval
lane_center = (left_x + right_x) / 2
cte_pixels  = (image_width / 2) − lane_center
cte_norm    = clamp(cte_pixels / (tracked_lane_width / 2), −1.0, +1.0)
```

**Sign convention:**

| CTE value | Meaning | Required action |
|---|---|---|
| Positive | Vehicle is to the **right** of center | Steer **left** |
| Negative | Vehicle is to the **left** of center | Steer **right** |
| 0.0 | Vehicle is centered | Maintain heading |

**EMA smoothing:**

```
ema_cte = 0.35 × raw_cte_norm + 0.65 × previous_ema_cte
```

**Dead zone:** errors smaller than `±0.02` are set to `0.0` to prevent jitter-induced micro-corrections on straight roads.

**Curvature formula:**

```
R = (1 + (2a·y + b)²)^(3/2) / |2a|
```

A radius above 10 000 px is treated as a straight road.

---

## Tunable Parameters

| Parameter | Location | Default | Description |
|---|---|---|---|
| `n_windows` | `SlidingWindowsLaneFitter` | `12` | Number of sliding window bands (bottom to top) |
| `margin` | `SlidingWindowsLaneFitter` | `40 px` | Half-width of each search window |
| `min_pixels` | `SlidingWindowsLaneFitter` | `20` | Minimum pixels to recenter a window |
| `lane_width_px` | `SlidingWindowsLaneFitter` | `180 px` | Initial expected lane width in BEV space |
| EMA alpha (polynomial) | `_smooth()` | `0.8` | Smoothing factor for lane coefficients (higher = less lag) |
| EMA alpha (CTE) | `_calculate_cte()` | `0.35 / 0.65` | Current / history weight for CTE smoothing |
| CTE dead zone | `_calculate_cte()` | `0.02` | Errors below this threshold are zeroed out |
| CTE eval depth | `_calculate_cte()` | `0.60 × H` | Vertical position where CTE is evaluated |
| Max curvature `|a|` | `_polyfit()` | `0.008` | Fits with higher curvature are rejected |
| Width tolerance | `fit()` | `±40%` | Allowed deviation from calibrated lane width |
| Width EMA | `fit()` | `0.95 / 0.05` | Previous / current weight for lane width calibration |
| BEV source points | `BEVTransform` | See table above | Road trapezoid corners in normalized camera coordinates |
| BEV destination points | `BEVTransform` | `[0.25–0.75] × H/W` | Output lane region in BEV space |