# Autonomous Driving Pipeline: Architecture Documentation

## 🏗️ Architectural Overview
This repository implements a modular, scalable, and highly testable pipeline for Autonomous Driving features, currently focused on Lane Keeping Assist (LFA).

The architecture is divided into a hardware interface (Hailo NPU), raw tensor decoding, domain-specific geometric logic, and vehicle control. This design ensures that adding future features (e.g., object detection) will not require rewriting the existing LFA logic.

## Directory Structure

```plaintext
pipeline/
├── main.py                     # Main orchestrator and execution loop
├── core/                       # Shared types and hardware infrastructure
│   ├── data_types.py           # Data contracts (Dataclasses)
│   └── hailo_engine.py         # Hailo-8 NPU wrapper
├── post_processing/            # Neural Network tensor decoding
│   ├── mask_filters.py         # Morphological filters (OpenCV)
│   └── yolo_decoder.py         # YOLOv8/v11-seg decoder
├─── LFA/                       # Domain Logic: Lane Following Assist
│   ├── geometry/               # BEV Transform and Sliding Windows
│   ├── tracking/               # Short-term memory and smoothing
│   └── visualization/          # HUD and telemetry rendering
├── object/                     #  Domain Logic: object detection
│   └── object_detection.py     # State machine
├── decision/                   # Decision & control logic
│   ├── PID_steering.py         # PID controller for steering
│   └── decision_fsm.py         # State machine
└── utils/                      # External interfaces and monitors
    ├── can_sender.py           # Physical CAN bus interface
    └── hw_monitor.py           # CPU and Thermal monitoring

```

## 📂 1. Core Infrastructure (core/)
This layer handles the foundational elements that are completely agnostic to the concept of "lanes" or "cars".

`data_types.py`: Defines data classes (e.g., LaneFitResult, TrackedLaneFit) used as contracts between modules(LFA and object_detection). This prevents circular dependencies and ensures strict type checking across the pipeline.

`hailo_engine.py`: A wrapper for the Hailo-8 AI accelerator. It implements a Python Context Manager to safely load the .hef model, allocate VDevice resources, and perform preprocessing (BGR to RGB, resizing). Exposes a clean .infer(frame) method.

## 📂 2. Post-Processing (post_processing/)

This layer translates raw, multi-dimensional mathematical tensors outputted by the neural network into human-readable computer vision formats (e.g., binary images or bounding boxes).

`yolo_decoder.py`: Contains the YoloSegDecoder class. It automatically discovers the output topology of the YOLOv8/v26-seg model, multiplies mask coefficients by prototype tensors, applies confidence thresholds, and outputs a clean uint8 binary mask.

`mask_filters.py`: Applies morphological operations (OpenCV MORPH_CLOSE and MORPH_OPEN) to the raw neural network mask to remove noise, fill gaps in the lane lines, and smooth the edges.

## 📂 3. Feature Modules: LFA (modules/LFA/)

This is the domain-specific layer. Everything here understands the physics and geometry of driving, roads, and lanes.

### `geometry/bev_transform.py`
Manages the Birds-Eye-View (BEV) perspective. Uses `cv2.getPerspectiveTransform` to warp the front-facing camera mask into a top-down view, allowing for accurate physical measurements.

### `sliding_windows.py`
The core computer vision algorithm for lane detection.
- Extracts histogram peaks to find lane bases.
- Slides tracking windows upward to follow curves.
- Fits 2nd-degree polynomials (y = ax^2 + bx + c) to the detected pixels.
- Calculates the Cross-Track Error (cte_norm), the normalized distance between the vehicle's center and the lane's center.

### `tracking/lane_identity_tracker.py`
Acts as the system's short-term memory. It maintains an **Exponential Moving Average (EMA)** of lane positions. It uses a similarity cost function to prevent **Identity Swaps** (where the AI confuses the left lane for the right lane during sharp turns or missing detections), ensuring a smooth and safe steering signal.

### `visualization/lane_visualiser.py`
Handles all HUD (Heads-Up Display) overlays. Draws the lane polygon, unwarps it back to the camera perspective, and renders telemetry text (CTE, FPS, Curvature Direction, Hardware Stats) on the screen for debugging.

## 📂 4. Decision & Utilities (decision/ & utils/)

### `decision/PID_steering.py`
Implements a Proportional-Integral-Derivative (PID) controller. It takes the `cte_norm` (error) from the LFA module and calculates the optimal steering correction.

### `utils/can_sender.py`
Interfaces with the vehicle's physical CAN bus to send the calculated steering commands.

### `utils/hw_monitor.py`
Monitors Raspberry Pi system health, reading CPU usage from `/proc/stat` and thermal data from `/sys/class/thermal`.

---

## 🔄 **5. The Orchestrator (main.py)**

The `main.py` script ties all modules together into a continuous data flow. It handles CLI arguments (camera vs. image mode, thresholds, display options) and executes the main while loop.

### The Per-Frame Data Flow:

1. **Capture:** Reads a YUV frame via `rpicam-vid` and converts to BGR.

2. **Inference:** HailoEngine runs the frame through the NPU.

3. **Decode:** YoloSegDecoder converts tensors to a binary mask.

4. **Filter:** MaskFilters cleans the mask noise.

5. **Warp:** BEVTransform flattens the mask to a top-down view.

6. **Fit & Measure:** SlidingWindowsLaneFitter finds the polynomials and calculates the CTE.

7. **Track:** LaneIdentityTracker smooths the polynomials and prevents left/right lane swaps.

8. **Control:** PID processes the CTE to generate a steering angle, sent via CanSender.

9. **Render:** `lane_visualiser.py` draws the results and sends the frame to the Wayland display sink via GStreamer.
