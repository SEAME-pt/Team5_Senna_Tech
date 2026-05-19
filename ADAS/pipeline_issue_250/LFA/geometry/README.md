# LFA Geometry

## Responsibility
Processes the lane mask to extract geometry useful for control.

## Stages
- `BEV Transform` - transforms the mask to top-down view
- `Sliding Windows` - locates lanes and fits polynomials
- `CTE` - extracts the normalized cross-track error

## Internal Documentation

### 04 - BEV Transform
Transforms the binary mask from front perspective to top-down view (`Bird's Eye View`), allowing measurement of real road distances.

#### Module
- `BEVTransform` - perspective transformation via `cv2.getPerspectiveTransform`

#### Input
| Field | Type | Shape |
|---|---|---|
| `binary_mask` | `numpy.ndarray uint8` | `(H, W)` |

#### Output
| Field | Type | Shape |
|---|---|---|
| `bev_mask` | `numpy.ndarray uint8` | `(H, W)` |

#### Notes
- Requires prior calibration (`src_points` and `dst_points`)
- To be filled during testing

### 05 - Sliding Windows
Locates left and right lanes in the BEV image and fits 2nd-degree polynomials to each.

#### Module
- `SlidingWindowsLaneFitter` - histogram + 9 sliding windows + `polyfit`

#### Input
| Field | Type | Shape |
|---|---|---|
| `bev_mask` | `numpy.ndarray uint8` | `(H, W)` |

#### Output
| Field | Type | Description |
|---|---|---|
| `fit_result` | `LaneFitResult` | Left/right polynomials + CTE |
| `fit_result.left_fit` | `numpy.ndarray` or `None` | Left polynomial coefficients |
| `fit_result.right_fit` | `numpy.ndarray` or `None` | Right polynomial coefficients |
| `fit_result.cte_norm` | `float` or `None` | Normalized CTE `[-1, 1]` |

#### Notes
- To be filled during testing

### 06 - CTE
Extracts the normalized cross-track error from the Sliding Windows result. Represents the vehicle's deviation from the lane center.

#### Input
| Field | Type | Description |
|---|---|---|
| `fit_result.cte_norm` | `float` or `None` | CTE calculated by Sliding Windows |

#### Output
| Field | Type | Description |
|---|---|---|
| `cte` | `float` | Normalized cross-track error `[-1, 1]` |

#### Behavior
- `0` - vehicle centered
- Negative - deviation to the left
- Positive - deviation to the right
- If `cte_norm` is `None` (lanes not detected), fallback to `0.0`

#### Notes
- To be filled during testing
