# Hailo Conversion Flow — Senna Edition

This section covers the full pipeline for converting segmentation models to
**HEF (Hailo Executable Format)** for inference on the Hailo-8 accelerator.

Two conversion flows are available depending on the model:

| Flow | Folder | Use when |
|---|---|---|
| **Model Zoo (hailomz)** | `convert_flow/` | YOLOv8-seg and other models supported by the Hailo Model Zoo |
| **BYOM (custom)** | `yolo26_seg/` | YOLO26-seg, YOLOv13 and any model not in the Model Zoo |

---

## Getting Started

### YOLOv8-seg — Model Zoo flow

The recommended entry point is:

```bash
./convert_flow/run_convert.sh
```

This script performs:
- model export to ONNX
- calibration image preparation
- training parameter loading from `args.yaml`, when available
- `nms_config.json` generation
- HEF compilation inside the Hailo container

Notes:
- The official project entry point is `./convert_flow/run_convert.sh`.
- Legacy root-level scripts for ONNX export, calibration preparation, and the old manual Docker flow were removed to avoid duplication and behavioral drift.
- The compilation step depends on the Hailo container being available. During environment setup or recovery, you may need to run `./convert_flow/run_hailo_docker.sh` first.

### YOLO26-seg — BYOM flow

The full automated pipeline for YOLO26n/s-seg is:

```bash
cd yolo26_seg/scripts/conversion
bash pipeline.sh <train_folder> <model_name> <input_size> [quant_mode] [cut_mode]
```

Example:
```bash
bash pipeline.sh yolov26nseg_cltusm_v yolo26n_seg_640 640 gpu 3outputs
```

This pipeline covers: ONNX export → ONNX cut (removes unsupported Tile nodes) →
translation → INT8 quantization → HEF compilation.

See `yolo26_seg/docs/06_complete_flow_reference.md` for the full step-by-step guide.

---

## Local Configuration

All scripts support local configuration through a `.env.hailo` file at the `convert_hailo/` root.

Use the example file as a starting point:

```bash
cp .env.hailo.example .env.hailo
```

Set the absolute paths and RPi5 address for your local machine in `.env.hailo`:
- `BASE_PROJECT` — path to the LKA model project
- `VENV_NAME` — path to the Hailo virtual environment
- `SHARED_DIR` — path to the Docker shared folder
- `CONTAINER_NAME` — Hailo Docker container name
- `DOCKER_IMAGE_NAME` — Hailo Docker image name
- `RUNS_BASE` — path to training runs folder (BYOM pipeline)
- `RPI5_HOST` — RPi5 SSH address (e.g. `root@<rpi5-ip>`)

This file is machine-local and must not be committed to the repository.

---

## External Prerequisites

Before using the Docker-based conversion flow, you need the Hailo AI Software Suite Docker image archive referenced by `DOCKER_TAR_FILE`.

In practice, this means:
- download the Hailo AI Software Suite Docker package from the Hailo Developer Zone
- place the downloaded tar archive where your local `.env.hailo` points to it
- keep `DOCKER_TAR_FILE` aligned with the actual downloaded filename

The Hailo documentation distributed with the suite is also available locally after setup inside `shared_with_docker/doc/`.

---

## Project Structure

- **`convert_flow/`**: Model Zoo conversion flow — scripts and documentation for the recommended YOLOv8-seg pipeline.
- **`yolo26_seg/`**: BYOM conversion flow — full pipeline for YOLO26n/s-seg custom models, including ONNX cut scripts, quantization, and inference test scripts for the RPi5.
- **`shared_with_docker/`**: folder shared with the Docker container — stores `best.onnx`, calibration images, helper scripts, `nms_config.json`, and generated compilation artifacts.
- **`docs/`**: supporting documentation and technical context for the Model Zoo flow.

Generated `.hef` artifacts are produced in `shared_with_docker/` during compilation and are not meant to be versioned.

---

## Documentation

### Model Zoo flow
```bash
docs/README.md
docs/01_run_convert.md
```

### BYOM flow (YOLO26-seg)
```bash
yolo26_seg/docs/06_complete_flow_reference.md   # full step-by-step
yolo26_seg/docs/07_yolo26_seg_study.md          # model study and architecture
yolo26_seg/docs/08_nano_rpi5_test.md            # RPi5 test guide
yolo26_seg/docs/NANO_TEST_GUIDE.txt             # quick reference
yolo26_seg/docs/Journey.md                      # full technical journey log
```

---

## Technologies Used

- **Ultralytics YOLO**: export and segmentation model structure (YOLOv8, YOLO26).
- **Hailo Dataflow Compiler / Hailo Model Zoo**: optimization and HEF compilation.
- **Docker**: isolated environment for the Hailo toolchain.

---

## Credits

Developed for the ADAS/LKA project, focused on preparing and compiling models for deployment on Hailo hardware.
