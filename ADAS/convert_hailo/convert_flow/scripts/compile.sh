#!/bin/bash

# ==============================================================================
# HAILO COMPILATION SPECIALIST - SENNA EDITION
# ==============================================================================
# This script runs INSIDE the Hailo Docker container.

# Use the first argument as MODEL_BASE, defaulting to `yolov8n_seg`
MODEL_BASE="${1:-yolov8n_seg}"

BASE_DIR="/local/shared_with_docker"
ONNX_MODEL="${BASE_DIR}/best.onnx"
CALIB_PATH="${BASE_DIR}/calibration_images"
HAILO_ARCH="hailo8"

# Create a temporary work directory inside the container to avoid permission errors
WORKDIR="/tmp/hailo_compile"
rm -rf "$WORKDIR" && mkdir -p "$WORKDIR"
cd "$WORKDIR"

echo "--------------------------------------------------"
echo "Starting HEF compilation (raw output mode)"
echo "Target model: ${MODEL_BASE}"
echo "ONNX model: ${ONNX_MODEL}"
echo "Calibration data: ${CALIB_PATH}"
echo "--------------------------------------------------"

# Check whether the required files exist
if [ ! -f "$ONNX_MODEL" ]; then
    echo "ERROR: ONNX model not found at ${ONNX_MODEL}"
    exit 1
fi

# Copy the ONNX model to WORKDIR so hailomz can read and write `.har` files next to it
cp "$ONNX_MODEL" .

# Run the official compilation without the `.alls` model script for raw output
hailomz compile "${MODEL_BASE}" \
                --ckpt "./best.onnx" \
                --calib-path "${CALIB_PATH}" \
                --hw-arch "${HAILO_ARCH}"

# Check the result
if [ $? -eq 0 ]; then
    echo "--------------------------------------------------"
    echo "Compilation succeeded. Moving artifacts to shared_with_docker..."
    
    # Move all generated `.hef` and `.har` files to the shared folder
    mv ./*.hef "$BASE_DIR/" 2>/dev/null
    mv ./*.har "$BASE_DIR/" 2>/dev/null
    
    echo "SUCCESS: HEF (raw output) generated successfully."
    ls -lh "${BASE_DIR}"/*.hef
    exit 0
else
    echo "--------------------------------------------------"
    echo "WARNING: Compilation failed."
    exit 1
fi
