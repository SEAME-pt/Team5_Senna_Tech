#!/bin/bash

# ==============================================================================
# MODEL QUANTIZATION - YOLO26-seg for Hailo-8
# ==============================================================================
# This script runs INSIDE the Hailo Docker container.
#
# Usage:
#   bash quantize.sh <model_name> <input_size> [mode]
#
# Available modes:
#   fast  - 64 images, no QFT, no GPU   (default for quick compilation validation)
#   cpu   - 1024 images, no QFT, forced CPU  (medium quality, slow)
#   gpu   - 1024 images, QFT batch=2, GPU    (maximum quality, recommended for production)
#
# Examples:
#   bash quantize.sh yolo26n_seg_640 640 fast
#   bash quantize.sh yolo26n_seg_640 640 cpu
#   bash quantize.sh yolo26n_seg_640 640 gpu
#
# Input:  <model_name>.har + calibration_images/
# Output: <model_name>_quantized.har

MODEL_NAME="${1:-yolo26n_seg_640}"
INPUT_SIZE="${2:-640}"
MODE="${3:-fast}"

DIR_BASE="/local/shared_with_docker"
HAR="${DIR_BASE}/${MODEL_NAME}.har"
CALIB="${DIR_BASE}/calibration_images"
QHAR="${DIR_BASE}/${MODEL_NAME}_quantized.har"

echo "--------------------------------------------------"
echo "Model Quantization"
echo "Model:      ${MODEL_NAME}"
echo "Input size: ${INPUT_SIZE}x${INPUT_SIZE}"
echo "Mode:       ${MODE}"
echo "HAR:        ${HAR}"
echo "Output:     ${QHAR}"
echo "--------------------------------------------------"

if [ ! -f "${HAR}" ]; then
    echo "ERROR: HAR not found at ${HAR}"
    exit 1
fi

if [ ! -d "${CALIB}" ]; then
    echo "ERROR: Calibration folder not found at ${CALIB}"
    exit 1
fi

# Fast mode: no GPU, 64 images, no QFT
if [ "${MODE}" = "fast" ]; then
    echo "FAST mode: 64 images, no QFT, CPU"
    CUDA_VISIBLE_DEVICES="" python3 << PYEOF
from hailo_sdk_client import ClientRunner
import numpy as np, os, glob
from PIL import Image

HAR       = "${HAR}"
QHAR      = "${QHAR}"
CALIB     = "${CALIB}"
INPUT_SIZE = ${INPUT_SIZE}

imgs = sorted(glob.glob(f"{CALIB}/*.jpg") + glob.glob(f"{CALIB}/*.png"))[:64]
print(f"Images: {len(imgs)}")
calib = np.zeros((len(imgs), INPUT_SIZE, INPUT_SIZE, 3), dtype=np.float32)
for i, p in enumerate(imgs):
    calib[i] = np.array(Image.open(p).convert("RGB").resize((INPUT_SIZE, INPUT_SIZE))) / 255.0

runner = ClientRunner(har=HAR)
runner.optimize(calib)
runner.save_har(QHAR)
size = os.path.getsize(QHAR) / (1024*1024)
print(f"\nQuantized HAR (fast): {QHAR} ({size:.1f} MB)")
PYEOF

# CPU mode: no GPU, 1024 images, no QFT
elif [ "${MODE}" = "cpu" ]; then
    echo "CPU mode: 1024 images, no QFT, forced CPU (slow)"
    CUDA_VISIBLE_DEVICES="" python3 << PYEOF
from hailo_sdk_client import ClientRunner
import numpy as np, os
from PIL import Image

HAR        = "${HAR}"
QHAR       = "${QHAR}"
CALIB      = "${CALIB}"
INPUT_SIZE  = ${INPUT_SIZE}
MODEL_NAME  = "${MODEL_NAME}"

files = [f for f in os.listdir(CALIB) if f.lower().endswith(('.jpg','.jpeg','.png'))][:1024]
print(f"Images: {len(files)}")
imgs = []
for i, f in enumerate(files):
    img = Image.open(os.path.join(CALIB, f)).convert("RGB").resize((INPUT_SIZE, INPUT_SIZE))
    imgs.append(np.array(img).astype(np.float32) / 255.0)
    if (i+1) % 200 == 0:
        print(f"  Loaded: {i+1}/{len(files)}")

calib_data = np.array(imgs)
print(f"Shape: {calib_data.shape}")

runner = ClientRunner(har=HAR)
WORK_DIR = f"/tmp/hailo_workdir_{MODEL_NAME}"
os.makedirs(WORK_DIR, exist_ok=True)
runner.optimize(calib_data, work_dir=WORK_DIR)
runner.save_har(QHAR)
size = os.path.getsize(QHAR) / (1024*1024)
print(f"\nQuantized HAR (cpu): {QHAR} ({size:.1f} MB)")
PYEOF

# GPU mode: with GPU, 1024 images, QFT batch=2
elif [ "${MODE}" = "gpu" ]; then
    echo "GPU mode: 1024 images, QFT batch=2, GPU (maximum quality)"
    python3 << PYEOF

from hailo_sdk_client import ClientRunner
import numpy as np, os
from PIL import Image

HAR        = "${HAR}"
QHAR       = "${QHAR}"
CALIB      = "${CALIB}"
INPUT_SIZE  = ${INPUT_SIZE}
MODEL_NAME  = "${MODEL_NAME}"

files = [f for f in os.listdir(CALIB) if f.lower().endswith(('.jpg','.jpeg','.png'))][:1024]
print(f"Images: {len(files)}")
imgs = []
for i, f in enumerate(files):
    img = Image.open(os.path.join(CALIB, f)).convert("RGB").resize((INPUT_SIZE, INPUT_SIZE))
    imgs.append(np.array(img).astype(np.float32) / 255.0)
    if (i+1) % 200 == 0:
        print(f"  Loaded: {i+1}/{len(files)}")

calib_data = np.array(imgs)
print(f"Shape: {calib_data.shape}")

alls_script = "post_quantization_optimization(finetune, policy=enabled, batch_size=2)\n"
runner = ClientRunner(har=HAR)
runner.load_model_script(alls_script)

WORK_DIR = f"/tmp/hailo_workdir_{MODEL_NAME}"
os.makedirs(WORK_DIR, exist_ok=True)
print(f"Work dir: {WORK_DIR}")

runner.optimize(calib_data, work_dir=WORK_DIR)
runner.save_har(QHAR)
size = os.path.getsize(QHAR) / (1024*1024)
print(f"\nQuantized HAR (gpu): {QHAR} ({size:.1f} MB)")
PYEOF

else
    echo "ERROR: Invalid mode '${MODE}'. Use: fast | cpu | gpu"
    exit 1
fi

exit $?
