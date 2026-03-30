# CARLA Simulator — Implementation in the SEA:ME Project

## Related Documentation

> 📖 **New to CARLA?** If you want to understand what CARLA is and what it is used for, [click here](https://github.com/SEAME-pt/Team5_Senna_Tech/tree/feature/carla/docs/CARLA-Simulator).

> 🚀 **Getting started?** To set up CARLA and launch the simulator for the first time, [see this guide](https://github.com/SEAME-pt/Team5_Senna_Tech/blob/feature/carla/docs/CARLA-Simulator/carla_initial_setup.md).

---

## Table of Contents

- [Overview](#overview)
- [Architecture](#architecture)
- [Class: CarlaEnvironment](#class-carlaenvironment)
  - [Key Responsibilities](#key-responsibilities)
  - [Synchronous Mode](#synchronous-mode)
  - [Dynamic Weather (Optional)](#dynamic-weather-optional)
- [Class: Vehicle](#class-vehicle)
  - [Ego Vehicle Configuration](#ego-vehicle-configuration)
  - [Sensors](#sensors)
  - [Image Processing](#image-processing)
  - [PID Steering Control](#pid-steering-control-pid_control_for_steering)
- [Dataset Generation](#dataset-generation)
  - [How It Works](#how-it-works)
  - [Variability](#variability)
  - [Enabling Dataset Generation](#enabling-dataset-generation)
- [Lane Detection in the Simulator](#lane-detection-in-the-simulator)
  - [Class: YOLOv8Detector](#class-yolov8detector)
  - [Multiple Models](#multiple-models)
- [PID Controller](#pid-controller)
  - [Class: PID](#class-pid)
  - [Anti-Windup and Clamping](#anti-windup-and-clamping)
  - [Control Loop](#control-loop)
- [Main Loop](#main-loop--carla_clientpy)
- [How to Run](#how-to-run)
- [Conclusion](#conclusion)

---

## Overview

This document describes the practical implementation of the CARLA Simulator within the SEA:ME autonomous vehicle project developed at 42 Porto. The simulator serves as a safe and controlled virtual environment for three key purposes:

- **Validating lane detection models** before deploying them on the physical prototype
- **Generating annotated datasets** (RGB images + segmentation masks) to improve model accuracy
- **Testing the full autonomous driving pipeline**, including real-time inference, post-processing via OpenCV, CTE calculation, and PID-based lateral control

The stack integrates CARLA's Python API, a YOLOv8 segmentation model, a custom LKA pipeline, and a PID controller — all running synchronously at a fixed timestep of 50ms (20Hz).

---

## Architecture

The simulation is structured around three main classes and one entry point:

```
carla_client.py         ← Entry point: orchestrates the main loop
├── CarlaEnvironment    ← Manages the CARLA world, settings, traffic
├── Vehicle             ← Spawns the ego vehicle, cameras, and applies control
├── YOLOv8Detector      ← Runs YOLOv8 segmentation inference
└── PID                 ← Computes steering output from CTE
```

The `LKAPipeline` (from the LKA module) handles image processing and CTE calculation, and is imported directly into `carla_client.py`.

---

## Class: `CarlaEnvironment`

**File:** `CarlaEnvironment.py`

Responsible for initialising and configuring the CARLA simulation world.

### Key Responsibilities

- Connects to the CARLA server at `localhost:2000`
- Loads the map `Town04_Opt` with selected map layers (Buildings, Foliage, Particles, etc.), then immediately unloads them to keep the environment lightweight and performance-focused
- Configures **synchronous mode** with a fixed timestep of `0.05s` (20 Hz), ensuring deterministic simulation ticks
- Manages the **Traffic Manager** on port `8000` also in synchronous mode
- Spawns **20 NPC vehicles** with autopilot enabled to simulate realistic traffic conditions

### Synchronous Mode

Synchronous mode is critical for this project. By calling `env.world.tick()` manually in the main loop, the simulation only advances when the Python client explicitly requests it. This guarantees that camera images are always aligned with the current simulation state before inference runs.

```python
settings.synchronous_mode = True
settings.fixed_delta_seconds = 0.05
self.world.apply_settings(settings)
self.traffic_manager.set_synchronous_mode(True)
```

### Dynamic Weather (Optional)

The class includes an `update_weather()` method that randomises cloudiness, fog density, and sun position each tick. This feature can be enabled in the main loop to generate training data under diverse lighting and visibility conditions, improving model robustness.

---

## Class: `Vehicle`

**File:** `Vehicle.py`

Manages the ego vehicle and its onboard sensors.

### Ego Vehicle Configuration

The vehicle spawned is an **Audi TT** (green, `RGB 50, 205, 50`) placed at spawn point index `1` of the map. Autopilot is disabled, as lateral control is handled entirely by the PID controller fed by the LKA pipeline.

### Sensors

Two cameras are attached to the vehicle, both positioned at `(x=1.5, z=1.7)` with a `−5°` pitch and a **102° horizontal FOV**, simulating a typical front-facing automotive camera:

| Sensor | Type | Purpose |
|--------|------|---------|
| `camera_actor` | `sensor.camera.rgb` | Provides colour frames for model inference |
| `camera_actor_seg` | `sensor.camera.semantic_segmentation` | Provides semantic labels for dataset generation |

Both cameras produce frames at **640×360 pixels**.

### Image Processing

**RGB Camera (`process_image`):**  
Raw BGRA data is reshaped and split into BGR and RGB arrays. The RGB frame is passed to the LKA pipeline for inference; the BGR frame is passed to the YOLOv8 detector. To generate a dataset, uncomment the following line:

```python
cv2.imwrite(f"dataset/images/{frame_id}.png", bgr)
```

**Semantic Segmentation Camera (`process_image_seg`):**  
The semantic camera produces per-pixel class labels. Lane markings correspond to **class ID 24** in the red channel. The binary mask is extracted as follows:

```python
lane_mask = seg[:, :, 2] == 24
lane_mask_img = lane_mask.astype(np.uint8) * 255
```

To save masks for dataset generation, uncomment:

```python
cv2.imwrite(f"dataset/masks/{frame_id}.png", lane_mask_img)
```

This pair of RGB image + binary lane mask constitutes a complete training sample for supervised segmentation model training.

### PID Steering Control (`pid_control_for_steering`)

After the LKA pipeline computes the normalised CTE, the `Vehicle` class applies it to the PID controller and sends a `VehicleControl` command to the simulator:

```python
control = carla.VehicleControl(
    throttle=0.5,
    steer=float(steering),
    brake=0.0
)
self.vehicle_actor.apply_control(control)
```

The current steering value is also rendered on the annotated frame for real-time visualisation.

---

## Dataset Generation

The CARLA implementation was used to generate a labelled dataset to train and improve the lane detection models. The process relies on the dual-camera setup described above.

### How It Works

1. The simulation runs with the ego vehicle in autopilot or manual mode
2. Every tick, the RGB camera saves a colour frame to `dataset/images/`
3. Simultaneously, the semantic segmentation camera extracts the binary lane mask and saves it to `dataset/masks/`
4. The filename is the CARLA frame ID, ensuring perfect alignment between image and mask

### Variability

The optional `update_weather()` method allows generating samples across different lighting and environmental conditions (cloudiness, fog density, sun angle), which significantly improves model generalisation.

### Enabling Dataset Generation

In `Vehicle.py`, uncomment the following lines:

```python
# In process_image():
cv2.imwrite(f"dataset/images/{frame_id}.png", bgr)

# In process_image_seg():
cv2.imwrite(f"dataset/masks/{frame_id}.png", lane_mask_img)
```

Ensure the directories `dataset/images/` and `dataset/masks/` exist before running.

---

## Lane Detection in the Simulator

**File:** `YOLOv8Detector.py`

Lane detection is performed by a **YOLOv8 segmentation model** fine-tuned on the dataset generated above.

### Class: `YOLOv8Detector`

The `YOLOv8Detector` class wraps Ultralytics' YOLO API and provides a single `infer()` method:

```python
results = self.model.predict(
    source=frame,
    imgsz=640,
    conf=0.3,
    device=0,       # GPU inference
    verbose=False
)
```

For each detected mask, the binary prediction is resized to the original frame resolution and overlaid in green with 40% opacity (`alpha=0.4`) using `cv2.addWeighted`. A unified `lane_mask` is built by taking the element-wise maximum across all detected lane instances.

### Multiple Models

The `carla_client.py` supports loading and comparing multiple model checkpoints simultaneously. During development, the following models were evaluated in parallel within the same simulation loop:

| Variable | Model File | Description |
|----------|-----------|-------------|
| `best` | `yolov26sseg_cltusm_v1.pt` | YOLOv26: best-performing model (so far) |
| `yolov8_detector` | `custom_yolo_v2.pt` | Earlier custom model |
| `yolov8n_detector` | `yolov8n_seg_3_datasets.pt` | YOLOv8n trained on 3 datasets |
| `yolov8s_detector` | `yolov8s_seg_3_datasets.pt` | YOLOv8s trained on 3 datasets |

Each model's output is displayed in a separate OpenCV window, enabling direct visual comparison during testing.

---

## PID Controller

**File:** `pid.py`

The PID controller computes the lateral steering correction from the Cross-Track Error (CTE) provided by the LKA pipeline.

### Class: `PID`

```
Steering = Kp × error + Ki × ∫error dt + Kd × Δerror/Δt
```

| Parameter | Value | Role |
|-----------|-------|------|
| `kp` | `0.3` | Proportional gain — main correction force |
| `ki` | `0.0` | Integral gain — disabled to avoid drift accumulation |
| `kd` | `0.001` | Derivative gain — dampens oscillation |

### Anti-Windup and Clamping

Both the integral accumulator and the final output are clamped symmetrically to `[-1.0, 1.0]`, matching CARLA's steering range:

```python
self.integral = clamp_symmetric(self.integral, self.integral_limit)  # limit = 1.0
output = clamp_symmetric(output, self.output_limit)                   # limit = 1.0
```

### Control Loop

The controller is updated every simulation tick (`dt = 0.05s`), with a target of `0.0` (vehicle centred on the lane):

```python
steering = pid.update(target=0.0, current=cte, dt=0.05)
```

A positive CTE means the vehicle is to the right of the lane centre; the controller returns a negative steering value to correct leftward, and vice versa.

---

## Main Loop — `carla_client.py`

The entry point orchestrates the full pipeline each tick:

```
world.tick()
    │
    ├─ image_queue  → BGR + RGB frames
    │
    ├─ LKAPipeline.process(rgb)  → fit_result (CTE), annotated frame
    │
    ├─ Vehicle.pid_control_for_steering(cte, pid, annotated)
    │       └─ PID.update() → steering value → VehicleControl applied
    │
    ├─ YOLOv8Detector.infer(bgr) → segmentation overlay
    │
    └─ cv2.imshow() → real-time visualisation
```

The loop runs until a `KeyboardInterrupt`, at which point all actors are destroyed, OpenCV windows are closed, and synchronous mode is disabled cleanly.

---

## How to Run

### Prerequisites

Before running the script, ensure the following are available on your system:

| Requirement | Version | Notes |
|-------------|---------|-------|
| CARLA Simulator | `0.9.16` | Must match the `carla` Python package version |
| Python | `3.10.x` | The venv was created with Python 3.10 |
| GPU drivers | CUDA-compatible | Required for YOLOv8 inference on `device=0` |

### 1. Activate the Virtual Environment

```bash
source ~/Team5_Senna_Tech/ADAS/CARLA-Simulator/venv/bin/activate
```

### 2. Install Dependencies

```bash
pip install -r ~/Team5_Senna_Tech/ADAS/CARLA-Simulator/requirements.txt
```

### 3. Launch the CARLA Server

In a **separate terminal**, navigate to your CARLA installation directory and launch the server in offscreen mode with Epic quality for maximum GPU utilisation and best visual fidelity:

```bash
cd path_to_CARLA_directory/CARLA_0.9.16/
./CarlaUE4.sh -RenderOffScreen -quality-level=Epic
```

Wait until the server is ready — you should see output indicating the world has been loaded. The server listens on `localhost:2000` by default.

> **Note:** `-RenderOffScreen` disables the CARLA viewport window, freeing GPU resources for rendering and inference. `-quality-level=Epic` enables the highest graphical fidelity, which produces more realistic training images and better lane marking visibility.

### 4. Run the Script

In your original terminal (with the venv active), navigate to the CARLA-Simulator directory and run the client:

```bash
cd ~/Team5_Senna_Tech/ADAS/CARLA-Simulator/
python3 carla_client.py
```

OpenCV windows will appear showing the LKA+PID annotated feed and the YOLOv8 segmentation output in real time. Press `Ctrl+C` to stop — the script will clean up all actors and disable synchronous mode automatically.

---

## Conclusion

The CARLA implementation in this project establishes a complete closed-loop autonomous driving testbench: the simulator generates photorealistic sensor data, the LKA pipeline computes lateral error, and the PID controller keeps the vehicle centred in the lane — all validated virtually before any code runs on the physical SEA:ME prototype. The same infrastructure was also used to build the training dataset that powers the lane detection models deployed on the real vehicle.
