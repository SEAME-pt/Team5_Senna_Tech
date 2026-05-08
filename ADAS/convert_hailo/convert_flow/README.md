# Hailo Conversion Orchestrator (`convert_flow`)

This directory contains the core of the automatic conversion process for the Hailo-8L chip.

## How to use the orchestrator

The `run_convert.sh` script is designed to be interactive and handle the full YOLOv8 model conversion workflow (Nano, Small, and so on).

This is the only recommended entry point for conversion. Equivalent legacy scripts at the project root were removed to avoid duplication.

Before using it, configure your local paths in `../.env.hailo` based on `../.env.hailo.example`.

The official project documentation is centralized in `../docs/README.md`.
The single source of truth for this script is `../docs/01_run_convert.md`.

### Automatic steps
1. **Validation:** checks whether the `.pt` model and the `hailo-env` virtual environment exist.
2. **ONNX Export:** converts the Ultralytics model to the intermediate ONNX format.
3. **INT8 Calibration:** uses the images in `shared_with_docker/calibration_images` for quantization.
4. **HEF Compilation:** calls the Docker environment and the **Hailo Model Zoo** to generate the final binary (`<model>.hef`).

## Internal organization

- **`scripts/`**:
  - `compile.sh`: the script that runs inside Docker to perform the compilation.

## External dependencies

- `./run_hailo_docker.sh`: helper script used to start the Hailo container when it is not available yet.
- `../shared_with_docker/`: shared volume used during export, calibration, and compilation.

## Technical notes

- **Supported model choices in the script:** `yolov8n_seg`, `yolov8s_seg`, `yolov8m_seg`, `yolov8l_seg`, and `yolov8x_seg`.
- **Raw Output:** the flow is configured for raw output, allowing custom and low-latency post-processing (as used in `TSHailo.py`).
- **NMS:** Non-Maximum Suppression is handled in the inference script, reducing latency on Hailo hardware.
