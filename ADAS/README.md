# ADAS — Autonomous Driving Assistance System

This directory contains all the development modules for the ADAS system of the Team5 SennaTech project, from simulator validation to the modular pipeline for real hardware (Raspberry Pi 5 + Hailo-8).

## Structure

### `CARLA-Simulator/`
Closed-loop virtual environment (CARLA 0.9.16) used for:
- Generating the training dataset (RGB image pairs + lane binary masks)
- Comparing YOLO architectures simultaneously.
- Validating the LKA + PID pipeline (20Hz, normalized CTE) before any `.pt` to `.hef` conversion and deployment on real hardware.

> Detailed documentation: [`CARLA-Simulator/README.md`](CARLA-Simulator/README.md), [`CARLA-First-Pass`](../docs/CARLA-Simulator/README.md)

### `convert_hailo/`
YOLO model conversion pipeline (`.pt` → ONNX → `.hef`) for deployment on the Hailo-8 accelerator. Supports the flow via Hailo Model Zoo (YOLOv8-seg) and BYOM flow for custom models (YOLO26-seg).

> Detailed documentation: [`convert_hailo/README.md`](convert_hailo/README.md)

### `LKA/`
PyTorch reference pipeline for lane detection and cross-track error (CTE) calculation. Receives an RGB frame and returns `cte_normalized [-1, 1]` for the PID controller via: YOLO-seg inference → morphological cleaning → BEV transformation → Sliding Windows + Polyfit. Includes an interactive BEV calibration tool and offline test scripts (image, video, webcam).

> Trained models available in `LKA_trained_models/` — production model: `yolov26sseg_cltusm_v1.pt`

### `Object_Detection/`
Object detection module running in production on the Hailo-8. Loads a `.hef` model (YOLO26n), reads camera frames via `rpicam-vid`, and performs manual post-processing (3-scale decode + NMS) to detect 13 custom classes: speed signs, traffic lights, stop signs, crosswalks, obstacles, and cars. Display via GStreamer `waylandsink`.

> Compiled models available in `models/`: `yolo26n_v1.hef`, `yolo26n_v2.hef`

### `pipeline/`
Production LFA (Lane Following Assist) pipeline running on RPi + Hailo-8. Layered architecture: `.hef` inference on NPU → YOLO-seg decoder → morphological filters → BEV → Sliding Windows → LaneIdentityTracker (EMA + lane swap prevention) → PID → CAN bus. Supports Virtual Lanes (estimates missing lane based on calibrated width) and `--remote` mode for streaming via stdout.

> Detailed documentation: [`pipeline/README.md`](pipeline/README.md)
