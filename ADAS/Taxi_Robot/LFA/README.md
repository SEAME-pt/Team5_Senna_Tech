# LFA — Lane Following Analysis

## Responsibility
Groups all lane-following analysis logic: BEV perspective transform, sliding-window lane fitting, and visualization. Takes a binary lane mask as input and produces polynomial lane fits + normalized cross-track error (CTE) consumed by the PID controller.

## Modules
- `geometry/bev_transform.py` — perspective warp from camera view to top-down (BEV)
- `geometry/sliding_windows.py` — histogram + sliding-window lane fitter with EMA smoothing and virtual lane estimation
- `visualization/lane_visualiser.py` — renders lane overlay back onto the original RGB frame via inverse BEV warp

## Submodules
- [geometry](geometry/README.md)
- [visualization](visualization/README.md)

## Data Contract
**Input:** `bev_mask` — `numpy.ndarray uint8 (H, W)` binary lane mask in BEV space.

**Output:** `LaneFitResult` — polynomial coefficients for left/right lanes, `cte_norm ∈ [-1.0, +1.0]`, curvature, virtual/found flags. Defined in `core/data_types.py`.

## Notes
- The BEV calibration (`DEFAULT_SRC`) was tuned for the imx708 mounted on the PiRacer with `--vflip --hflip`. Different mounting positions require recalibration.
