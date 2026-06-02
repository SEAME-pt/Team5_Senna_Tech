#!/bin/bash

# ==============================================================================
# TRANSLATION / PARSING - ONNX to HAR
# ==============================================================================
# This script runs INSIDE the Hailo Docker container.
# Translates the cut ONNX to HAR (Hailo Archive) format.
#
# Usage:
#   bash translate.sh <model_name> <input_size>
#
# Examples:
#   bash translate.sh yolo26s_seg_416 416
#   bash translate.sh yolo26s_seg 640
#
# Input:  best_cut.onnx
# Output: <model_name>.har

MODEL_NAME="${1:-yolo26s_seg_416}"
INPUT_SIZE="${2:-416}"

DIR_BASE="/local/shared_with_docker"
ONNX="${DIR_BASE}/best_cut.onnx"
HAR="${DIR_BASE}/${MODEL_NAME}.har"

echo "--------------------------------------------------"
echo "Translation ONNX -> HAR"
echo "Model:  ${MODEL_NAME}"
echo "Input:  ${ONNX}"
echo "Output: ${HAR}"
echo "Size:   ${INPUT_SIZE}x${INPUT_SIZE}"
echo "--------------------------------------------------"

if [ ! -f "${ONNX}" ]; then
    echo "ERROR: ONNX not found at ${ONNX}"
    exit 1
fi

python3 << PYEOF
from hailo_sdk_client import ClientRunner
import os

ONNX = "/local/shared_with_docker/best_cut.onnx"
HAR = "${HAR}"
MODEL_NAME = "${MODEL_NAME}"
INPUT_SIZE = ${INPUT_SIZE}

print("Initializing ClientRunner...")
runner = ClientRunner(hw_arch="hailo8")

print("Translating ONNX model...")
runner.translate_onnx_model(
    ONNX,
    MODEL_NAME,
    net_input_shapes={"images": [1, 3, INPUT_SIZE, INPUT_SIZE]}
)

runner.save_har(HAR)
size = os.path.getsize(HAR) / (1024*1024)
print(f"\n--------------------------------------------------")
print(f"HAR saved: {HAR} ({size:.1f} MB)")
print(f"--------------------------------------------------")
PYEOF

exit $?
