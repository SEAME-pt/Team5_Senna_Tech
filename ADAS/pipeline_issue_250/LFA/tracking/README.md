# LFA Tracking

## Index
- [Overview](#overview)
- [Classes](#classes)
  - [LaneIdentityTracker](#laneidentitytracker)
- [Data Contract](#data-contract)
- [Debug](#debug)
- [Notes](#notes)

## Overview
Ensures consistent lane identity (left/right) across frames. The sliding windows detector can occasionally swap the left and right lanes, particularly on tight curves. This module corrects that by maintaining exponential moving averages (EMA) of each lane's expected position and requiring multiple consecutive frames to confirm a swap before applying it.

## Classes

### `LaneIdentityTracker`

#### `__init__(image_width, image_height, ema_alpha, swap_confirm_frames, position_weight)`

| Parameter | Default | Description |
|---|---|---|
| `image_width` | `640` | Frame width in pixels |
| `image_height` | `360` | Frame height in pixels |
| `ema_alpha` | `0.25` | EMA smoothing factor (higher = faster adaptation) |
| `swap_confirm_frames` | `8` | Consecutive frames required to confirm a swap |
| `position_weight` | `0.7` | Weight of position vs. shape in the similarity function |

#### `assign(fit_result) → TrackedLaneFit`
Main entry point. Receives a raw `LaneFitResult` and returns a `TrackedLaneFit` with consistent identity.

**Behavior**
1. On the first frame, initialises the EMA from the detected positions.
2. On subsequent frames, computes the assignment cost for normal and swapped orders.
3. If a swap is suspected, increments a counter — the swap is only applied after `swap_confirm_frames` consecutive detections.
4. Updates the EMAs with the assigned fits.

**Output** — `TrackedLaneFit` (see `core/README.md`).

#### `_initialize_first_frame(lf, rf, li, ri)`
Assigns left/right identity on the first detection based on horizontal position relative to frame centre.

#### `_assign_identity(lf, rf, li, ri)`
Computes cost_A (normal) and cost_B (swapped) and selects the lower-cost assignment.

#### `_similarity(fit_new, fit_ref, x_new, x_ref) → float`
Combines position distance (normalised by frame width) and shape distance (polynomial coefficients). Position is weighted at `position_weight` (default 70%).

#### `_update_ema(lf, rf)`
Updates the EMA for each lane using `EMA_new = alpha * fit_new + (1 - alpha) * EMA_previous`.

## Data Contract
| Field | Type | Meaning |
|---|---|---|
| Input `fit_result` | `LaneFitResult` | Raw fit from `SlidingWindowsLaneFitter` |
| Output | `TrackedLaneFit` | Identity-stabilised lane fits |

## Debug
No `debug` flag. The `swap_pending` field in `TrackedLaneFit` signals when a potential swap is detected but not yet confirmed — this can be used by `main` or visualisation to flag uncertain frames.

## Notes
- The EMA is only updated when a lane is actually detected — `None` fits do not decay the EMA.
- The swap counter decays by 1 each frame where no swap is suspected, preventing false positives from accumulating.
- `swap_confirm_frames=8` means the vehicle needs ~0.5s at 15 FPS of consistent swap evidence before the identity is corrected.
