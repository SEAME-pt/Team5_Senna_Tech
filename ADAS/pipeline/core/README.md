# Core Module

## Index
- [Overview](#overview)
- [Data Types](#data-types)
  - [LaneFitResult](#lanefitresult)
- [Usage](#usage)
- [Notes](#notes)

## Overview
The `core/` module holds shared data contracts used across multiple pipeline stages. It contains no executable logic — only dataclass definitions that represent the results produced and consumed between modules.

This separation ensures that modules like `LFA`, `decision`, and `visualization` share a common, well-defined interface without depending on each other directly.

## Data Types

### `LaneFitResult`
Contains all data resulting from lane detection and polynomial fitting for a single frame.

| Field | Type | Description |
|---|---|---|
| `left_fit` | `Optional[np.ndarray]` | Polynomial coefficients `[a, b, c]` for the left lane (`x = a·y² + b·y + c`) |
| `right_fit` | `Optional[np.ndarray]` | Same for the right lane |
| `cte_pixels` | `Optional[float]` | Lateral error in pixels (positive = vehicle to the right of centre) |
| `cte_norm` | `Optional[float]` | Lateral error normalised between `-1.0` and `+1.0` |
| `curvature_px` | `Optional[float]` | Radius of curvature in pixels (>10000 = straight road) |
| `left_found` | `bool` | `True` if the left lane was directly detected (not virtual) |
| `right_found` | `bool` | `True` if the right lane was directly detected (not virtual) |
| `debug_image` | `Optional[np.ndarray]` | Debug image with sliding windows drawn, or `None` |
| `left_is_virtual` | `bool` | `True` if the left lane was estimated from the right |
| `right_is_virtual` | `bool` | `True` if the right lane was estimated from the left |
| `swap_pending` | `bool` | Reserved field — not actively used |

**Produced by:** `LFA/geometry/sliding_windows.py`
**Consumed by:** `LFA/visualization/`, `decision/`, `main.py`

## Usage
```python
from core.data_types import LaneFitResult
```

## Notes
- `core/` contains no hardware dependencies and no executable pipeline logic.
- If a new shared data contract is needed between modules, it should be defined here.
