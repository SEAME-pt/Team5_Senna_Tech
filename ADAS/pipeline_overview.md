# ADAS Pipeline — Overview

## Step 1 — Data Input (Camera / Frames)

The first stage of the pipeline is capturing frames that will be used for inference by the detection model. The frame source and input flow vary depending on the execution environment:

- **CARLA Simulator** — RGB virtual camera (640×360, 102° FOV), frames captured directly via the CARLA Python API. The model used is `.pt` (PyTorch), running on a PC.
- **Physical Hardware (RPi + Hailo-8)** — Physical camera captured via `rpicam-vid` in YUV420 format, converted to BGR. The model used is `.hef`, compiled and optimized for the Hailo-8 accelerator.

## Step 2 — Inference

The captured frame is processed by the detection model. The flow varies depending on the environment:

- **`.pt` (PyTorch / CARLA)** — The frame goes directly to the model via Ultralytics (`model.predict()`), which internally handles inference, decoding, NMS, and mask extraction.
- **`.hef` (Hailo-8 / RPi)** — The frame is pre-processed (resized, BGR→RGB conversion) and sent to the NPU via `HailoEngine.infer()`, which returns raw tensors.

## Step 3 — Tensor Post-processing (only for `.hef`)

This stage applies only to `.hef`, as Ultralytics (`.pt`) internally handles decoding, NMS, and mask extraction. For `.hef`, the Hailo accelerator returns raw tensors that need to be manually interpreted through two steps:

- **`YoloSegDecoder`** — Discovers the model's output topology, multiplies mask coefficients by prototype tensors, applies a confidence threshold, and returns a `uint8` binary mask.
- **`MaskFilters`** — Cleans the mask with morphological operations (MORPH_CLOSE + MORPH_OPEN) to fill gaps in dashed lines and remove isolated noise.

## Step 4 — BEV Transform (Bird's Eye View)

BEV is the top-down view of the road. This stage is necessary because, in a front-facing image, lanes appear to converge in the distance due to perspective, making it impossible to measure real distances and calculate CTE accurately. By transforming the image into a top-down view, lanes become parallel, and pixels have a direct relationship with real meters, allowing Sliding Windows to function accurately.

For this transformation to be possible, **prior calibration** is required — defining 4 points (`src_points`) on the road in the front frame that form a trapezoid, and the corresponding rectangle in BEV (`dst_points`). This calibration is done with the `calibrar.py` tool and depends on the camera's physical position — if the camera position changes, recalibration is necessary.

The transformation is applied via `cv2.getPerspectiveTransform` (`BEVTransform.warp()`).

## Step 5 — Sliding Windows + Polyfit

With the BEV image, the algorithm locates the left and right lanes through three steps: a histogram to find the lane bases in the lower half of the image, 9 sliding windows that move from bottom to top following each lane's pixels, and fitting a 2nd-degree polynomial (`x = ay² + by + c`) to each lane with the collected pixels.

## Step 6 — CTE (Cross-Track Error)

CTE (Cross-Track Error) is the normalized lateral error `[-1, 1]` representing the vehicle's deviation from the lane center. It is calculated by evaluating the two polynomials at the base of the image to obtain the `x` position of each lane, calculating the center between them, and comparing it with the vehicle's center (middle of the image). The difference is normalized by the lane width — `0` means the vehicle is centered, negative values indicate deviation to the left, and positive values indicate deviation to the right.

## Step 7 — PID (Steering Controller)

The PID controller receives the CTE and calculates the steering correction angle. It consists of three components:

- **P (Proportional)** — Reacts to the current error. If the CTE is large, it corrects significantly. If it's small, it corrects slightly.
- **I (Integral)** — Corrects accumulated errors over time. Prevents the vehicle from being systematically deviated to one side.
- **D (Derivative)** — Smooths the correction by predicting error trends. Prevents abrupt steering oscillations.

The result is a normalized steering value `[-1, 1]`. The gains used in the project are `kp=1.2`, `ki=0.4`, `kd=0.35`.

## Step 8 — CAN Bus

The CAN Bus (Controller Area Network) is a vehicle communication protocol that connects the car's electronic components. `CanSender` receives the steering value calculated by the PID and sends it over the CAN bus to address `0x110`. The servo control component receives this command and applies the physical correction to the vehicle — it is the bridge between the Python software on the RPi and the PiRacer's physical hardware.
