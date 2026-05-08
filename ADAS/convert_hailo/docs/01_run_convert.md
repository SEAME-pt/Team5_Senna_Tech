# `run_convert.sh`

This document is the single source of truth for the `./convert_flow/run_convert.sh` flow.

## Purpose

`run_convert.sh` is the official entry point for converting a trained YOLOv8-seg model (`best.pt`) into a Hailo-ready HEF pipeline artifact set.

It handles:
- local environment loading from `.env.hailo`
- training run selection
- model scale selection (`n`, `s`, `m`, `l`, `x`)
- training parameter reuse from `args.yaml`
- ONNX export
- calibration dataset preparation
- `nms_config.json` generation
- Docker-side HEF compilation

## Expected project layout

The script expects the training project to follow this structure:

- `${BASE_PROJECT}/runs/<run>/weights/best.pt`
- `${BASE_PROJECT}/runs/<run>/args.yaml` optional
- `${BASE_PROJECT}/datasets/`

The local conversion workspace is expected to contain:

- `hailo-env/`
- `shared_with_docker/`
- `convert_flow/scripts/compile.sh`

## Supported environment variables

These values can be provided through `.env.hailo`:

- `BASE_PROJECT`
- `VENV_NAME`
- `SHARED_DIR`
- `CONTAINER_NAME`
- `DOCKER_IMAGE_NAME`
- `DOCKER_TAR_FILE`

Current defaults in the script:

- `BASE_PROJECT=${HOME}/Documents/ADAS/LKA_model`
- `VENV_NAME=${ROOT_DIR}/hailo-env`
- `SHARED_DIR=${ROOT_DIR}/shared_with_docker`
- `CONTAINER_NAME=hailo8_ai_sw_suite_2025-10_container`

## Required external download

This flow assumes you already have access to the Hailo AI Software Suite Docker package referenced by `DOCKER_TAR_FILE`.

That archive is not produced by this repository. It must be downloaded separately from the Hailo Developer Zone and stored locally so `convert_flow/run_hailo_docker.sh` can load it with Docker.

After the suite is installed, Hailo's bundled documentation is also available locally inside:

```text
shared_with_docker/doc/
```

## What the script actually does

### 1. Load configuration

If `${ROOT_DIR}/.env.hailo` exists, the script sources it before resolving fallbacks.

### 2. Ask for the training run

The script prompts for the folder name under `${BASE_PROJECT}/runs/`.

This value is required. The script does not apply a default run name.

### 3. Ask for the YOLOv8-seg scale

The script accepts:

- `1` or `n` -> `yolov8n_seg`
- `2` or `s` -> `yolov8s_seg`
- `3` or `m` -> `yolov8m_seg`
- `4` or `l` -> `yolov8l_seg`
- `5` or `x` -> `yolov8x_seg`

Invalid input falls back to `yolov8n_seg`.

### 4. Validate the local setup

The script checks:

- the model file exists at `${BASE_PROJECT}/runs/<run>/weights/best.pt`
- the Python virtual environment exists at `${VENV_NAME}`

It also resets `shared_with_docker/` for a fresh run while preserving the expected directory structure:

- `shared_with_docker/calibration_images/`
- `shared_with_docker/scripts/`

### 5. Reuse training parameters from `args.yaml`

If present, the script reads:

- `imgsz`
- `conf`
- `iou`
- `nc`

Fallbacks used when values are missing:

- `imgsz=640`
- `conf=0.25`
- `iou=0.45`
- `nc=1`

### 6. Export ONNX

The script activates the local Python environment and runs:

```bash
yolo export model="${MODEL_PT}" format=onnx simplify=true imgsz=${TRAIN_IMGSZ} opset=12
```

The generated `best.onnx` is moved to:

```text
shared_with_docker/best.onnx
```

### 7. Prepare calibration data

The script copies a random subset of dataset images into:

```text
shared_with_docker/calibration_images/
```

Current amount:

```text
1024 images
```

### 8. Generate `nms_config.json`

The script writes:

```text
shared_with_docker/nms_config.json
```

using:

- `TRAIN_CONF`
- `TRAIN_IOU`
- `NUM_CLASSES`
- `meta_arch=yolov8`

### 9. Restore the Docker-side compile script

The versioned compile script:

```text
convert_flow/scripts/compile.sh
```

is copied to:

```text
shared_with_docker/scripts/compile.sh
```

This copy is generated at runtime and should not be treated as a manually maintained source file.

### 10. Optionally start HEF compilation

If the user confirms, the script:

- checks whether the configured container is already running
- starts it if needed
- runs:

```bash
sudo docker exec -it "${CONTAINER_NAME}" /bin/bash -c "/local/shared_with_docker/scripts/compile.sh ${MODEL_BASE}"
```

## Manual equivalent

Use this only for debugging. The official path remains `./convert_flow/run_convert.sh`.

### Prepare configuration

```bash
cp .env.hailo.example .env.hailo
. ./.env.hailo
```

### Export to ONNX

```bash
source "${VENV_NAME}/bin/activate"
yolo export model="${BASE_PROJECT}/runs/YOUR_RUN/weights/best.pt" format=onnx simplify=true imgsz=640 opset=12
mkdir -p "${SHARED_DIR}"
mv "${BASE_PROJECT}/runs/YOUR_RUN/weights/best.onnx" "${SHARED_DIR}/best.onnx"
```

### Prepare calibration

```bash
mkdir -p "${SHARED_DIR}/calibration_images" "${SHARED_DIR}/scripts"
find "${BASE_PROJECT}/datasets" -type f \( -iname "*.jpg" -o -iname "*.jpeg" -o -iname "*.png" \) | shuf | head -n 1024 | while read -r img; do cp "$img" "${SHARED_DIR}/calibration_images/"; done
cp ./convert_flow/scripts/compile.sh "${SHARED_DIR}/scripts/compile.sh"
chmod +x "${SHARED_DIR}/scripts/compile.sh"
```

### Start the Hailo container

```bash
sudo ./convert_flow/run_hailo_docker.sh
```

### Compile manually

```bash
sudo docker exec -it "${CONTAINER_NAME:-hailo8_ai_sw_suite_2025-10_container}" /bin/bash -c "/local/shared_with_docker/scripts/compile.sh yolov8n_seg"
```

Replace `yolov8n_seg` with the required scale.

## Real dependencies

- a working Python virtual environment with `ultralytics`
- a training workspace under `BASE_PROJECT`
- a writable `shared_with_docker/` directory
- Docker available on the host
- `sudo` access for Docker commands
- the Hailo AI Software Suite Docker tar archive downloaded from the Hailo Developer Zone

## Current limitations

- the training project layout is fixed
- `hailo8` is hardcoded in the compile script
- compilation remains interactive
- the flow produces raw output and depends on post-processing outside the `.hef`

## Expected outputs

After a successful full run, the generated artifacts live under `shared_with_docker/`:

- `best.onnx`
- `calibration_images/`
- `nms_config.json`
- generated `.har`
- generated `.hef`
