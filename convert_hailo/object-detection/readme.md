# 🏁 Hailo YOLO Object Detection Conversion Pipeline

This repository provides a **complete pipeline to convert a trained YOLO model (e.g. YOLO26)** into a Hailo-compatible `.hef` binary using:

* ONNX export
* INT8 calibration
* Hailo Model Zoo compilation (`hailomz`)

---

## 📁 Project Structure

```bash
convert_hailo/
├── object-detection/
│   └── run_convert.sh
│   └── run_hailo_docker.sh   

├── shared_with_docker/      # Shared folder (host <-> container)
├── hailo-env/               # Python virtual environment
├── .env.hailo.object        # Environment configuration (CRITICAL)
```

---

## 🚀 How to Run

From the root folder:

```bash
cd ~/convert_hailo
./object-detection/run_convert.sh
```

## ⚙️ Environment Configuration (`.env.hailo.object`)

This file defines all paths and runtime variables used by the pipeline.

### Example:

```bash
export DOCKER_IMAGE_NAME=hailo8_ai_sw_suite_2025-10:1
export DOCKER_TAR_FILE=hailo8_ai_sw_suite_docker_2025-10.tar.gz

# Base project
export BASE_PROJECT="$HOME/ADAS/Object-Detection"

# Python environment (Ultralytics + ONNX)
export VENV_NAME="$HOME/convert_hailo/hailo-env"

# Docker container
export CONTAINER_NAME="hailo8_ai_sw_suite_2025-10_container"

# Shared directory (MUST match Docker mount)
export SHARED_DIR="$HOME/convert_hailo/shared_with_docker"

# Dataset location (custom)
export DATASETS_DIR="$HOME/ADAS/Object-Detection/datasets/merged_all_datasets/train/images"

# Calibration size
export NUM_CALIB_IMAGES=1024
```

---

### 🔴 Common failure cases:

| Problem                         | Cause                    |
| ------------------------------- | ------------------------ |
| `find: '' No such file`         | `DATASETS_DIR` not set   |
| `head: invalid number of lines` | `NUM_CALIB_IMAGES` empty |
| ONNX not found                  | wrong `BASE_PROJECT`     |
| Compilation fails               | wrong `SHARED_DIR` mount |
| No calibration images           | wrong dataset path       |

---

## 🔗 Critical Dependency: Docker Mount

Your container **must match this mapping**:

```bash
-v $HOME/convert_hailo/shared_with_docker:/local/shared_with_docker
```

And in `.env.hailo.object`:

```bash
export SHARED_DIR="$HOME/convert_hailo/shared_with_docker"
```

If these don’t match →
❌ Hailo will not find ONNX or calibration images

---

## 📊 Requirements

* Docker installed and running
* Hailo AI Software Suite container
* Python venv with:

  * ultralytics
  * onnx
* Dataset with sufficient images (≥ 1024 recommended)

---

