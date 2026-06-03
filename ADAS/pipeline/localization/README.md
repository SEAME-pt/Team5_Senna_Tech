# ArUco Localization

## Index
- [Overview](#overview)
- [Functions](#functions)
  - [`ArucoDetector.detect`](#arucodetectordetectframe--dict--none)
- [Data Contract](#data-contract)
- [Calibration](#calibration)
- [Return Format](#return-format)
- [Notes](#notes)

---

## Overview
The `localization/aruco` module is responsible for detecting ArUco markers in the camera frame and estimating the **closest marker distance in meters** using a simplified pinhole camera model.

It is designed for **lightweight localization without full camera calibration**, making it suitable for real-time robot navigation and waypoint detection in the SEA:ME pipeline.

---

## Functions

### `ArucoDetector.detect(frame) → dict | None`

Detects ArUco markers in the input frame and returns the closest marker based on estimated distance.

### Behavior
1. Detects ArUco markers using OpenCV `ArucoDetector`.
2. Extracts corner coordinates for each detected marker.
3. Estimates pixel width using the top edge of the marker.
4. Computes distance using a simplified pinhole camera model:
   `distance = (TAG_SIZE_M * FOCAL_LENGTH) / pixel_width`
5. Selects the **closest marker (minimum distance)**.
6. Returns only one result (the closest marker).

### Inputs
| Field | Type | Description |
| :--- | :--- | :--- |
| `frame` | `numpy.ndarray` | Input camera frame (BGR or RGB depending on pipeline) |

### Output
Returns a **single dictionary** representing the closest detected marker:

| Field | Type | Description |
| :--- | :--- | :--- |
| `id` | `int` | ArUco marker ID |
| `distance` | `float` | Estimated distance in meters (rounded to 2 decimals) |

*If no markers are detected, returns `None`.*

---

## Data Contract

| Field | Type | Meaning |
| :--- | :--- | :--- |
| `frame` | `numpy.ndarray` | Input image from camera |
| `corners` | `list[np.ndarray]` | 4 corner points of each marker |
| `pixel_width` | `float` | Estimated marker size in pixels |
| `distance` | `float` | Estimated distance in meters |
| `output` | `dict | None` | Closest marker data or None |

---

## Calibration

The distance estimation relies on two key constants:

* **`TAG_SIZE_M`**: Physical size of the printed ArUco marker in meters.
    * *Example:* 4 cm tag → 0.04
* **`FOCAL_LENGTH`**: Camera focal length expressed in pixel units (NOT mm). It is estimated using a known distance:
    `FOCAL_LENGTH = (pixel_width * real_distance) / real_tag_size`

### Practical Calibration Method
1. Place a known ArUco marker at a known distance (e.g., 10 cm).
2. Measure its pixel width in the image.
3. Compute `FOCAL_LENGTH` using the formula above.
4. Fix the value in your configuration code.

---

## Return Format

### Single detection (closest marker)
```
{
    "id": 7,
    "distance": 0.82
}
```

### No Markers detected
```
{
    "id": "None",
    "distance": "None"
}
```