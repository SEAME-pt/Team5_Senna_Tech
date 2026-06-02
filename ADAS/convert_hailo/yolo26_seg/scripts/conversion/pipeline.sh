#!/bin/bash

# ==============================================================================
# FULL PIPELINE - best.pt -> HEF for Hailo-8
# ==============================================================================
# Runs ON THE HOST (outside the container).
# Exports ONNX and runs cut -> translate -> quantize -> compile inside the container.
#
# Usage:
#   bash pipeline.sh <train_folder> <model_name> <input_size> [quant_mode] [cut_mode]
#
# If quant_mode and cut_mode are not provided, the script asks interactively.
#
# Examples:
#   bash pipeline.sh yolov26nseg_cltusm_v yolo26n_seg_640 640
#   bash pipeline.sh yolov26sseg_cltusm   yolo26s_seg_640 640 gpu 10outputs
#   bash pipeline.sh yolov26nseg_cltusm_v yolo26n_seg_640 640 gpu 3outputs

# Load local configuration from .env.hailo
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ENV_FILE="${SCRIPT_DIR}/../../../.env.hailo"
if [ -f "${ENV_FILE}" ]; then
    # shellcheck source=../../../.env.hailo
    source "${ENV_FILE}"
else
    echo "WARNING: ${ENV_FILE} not found. Set environment variables manually."
fi

usage() {
    echo "Usage: bash pipeline.sh <train_folder> <model_name> <input_size> [quant_mode] [cut_mode]"
    echo ""
    echo "  train_folder  Training folder name under runs/ (e.g. yolov26nseg_cltusm_v)"
    echo "  model_name    Hailo model name               (e.g. yolo26n_seg_640)"
    echo "  input_size    Input resolution               (e.g. 640)"
    echo "  quant_mode    fast | cpu | gpu               (interactive if omitted)"
    echo "  cut_mode      10outputs | 3outputs           (interactive if omitted)"
    echo ""
    echo "  cut_mode=10outputs -> cut_onnx_small.sh + compile greedy 0.6  (yolo26s)"
    echo "  cut_mode=3outputs  -> cut_onnx_nano.sh  + compile greedy 0.9  (yolo26n)"
    exit 1
}

if [ $# -lt 3 ]; then
    usage
fi

TRAIN_FOLDER="$1"
MODEL_NAME="$2"
INPUT_SIZE="$3"
QUANT_MODE="${4:-}"
CUT_MODE="${5:-}"

# Validate required environment variables
: "${RUNS_BASE:?RUNS_BASE not set. Configure it in .env.hailo}"
: "${SHARED_DIR:?SHARED_DIR not set. Configure it in .env.hailo}"
: "${VENV_NAME:?VENV_NAME not set. Configure it in .env.hailo}"
: "${CONTAINER_NAME:?CONTAINER_NAME not set. Configure it in .env.hailo}"
: "${DOCKER_IMAGE_NAME:?DOCKER_IMAGE_NAME not set. Configure it in .env.hailo}"
: "${RPI5_HOST:?RPI5_HOST not set. Configure it in .env.hailo}"

BEST_PT="${RUNS_BASE}/${TRAIN_FOLDER}/weights/best.pt"
HAILO_ENV="${VENV_NAME}/bin/activate"

# --- Initial checks ---
if [ ! -f "${BEST_PT}" ]; then
    echo "ERROR: best.pt not found at ${BEST_PT}"
    echo "Available folders:"
    ls "${RUNS_BASE}/"
    exit 1
fi

if [ ! -d "${SHARED_DIR}/calibration_images" ]; then
    echo "ERROR: Calibration folder not found at ${SHARED_DIR}/calibration_images"
    exit 1
fi

# --- Interactive menu: cut mode ---
if [ -z "${CUT_MODE}" ]; then
    echo ""
    echo "ONNX cut mode:"
    echo "  1) 10outputs - cut_onnx_small.sh + compile greedy 0.6  (yolo26s - small)"
    echo "  2) 3outputs  - cut_onnx_nano.sh  + compile greedy 0.9  (yolo26n - nano)"
    read -rp "Option [1]: " CUT_OPT
    case "${CUT_OPT}" in
        2) CUT_MODE="3outputs" ;;
        *) CUT_MODE="10outputs" ;;
    esac
fi

# --- Interactive menu: quantization mode ---
if [ -z "${QUANT_MODE}" ]; then
    echo ""
    echo "Quantization mode:"
    echo "  1) fast - 64 images, no QFT   (quick compilation validation)"
    echo "  2) cpu  - 1024 images, no QFT"
    echo "  3) gpu  - 1024 images, QFT batch=2, GPU  (production, recommended)"
    read -rp "Option [3]: " QUANT_OPT
    case "${QUANT_OPT}" in
        1) QUANT_MODE="fast" ;;
        2) QUANT_MODE="cpu" ;;
        *) QUANT_MODE="gpu" ;;
    esac
fi

# --- Compilation parameters by cut_mode ---
if [ "${CUT_MODE}" = "3outputs" ]; then
    COMPILE_UTIL="0.9"
    COMPILE_STRATEGY="greedy"
    CUT_DESC="3 outputs (cut_onnx_nano) — yolo26n"
else
    CUT_MODE="10outputs"
    COMPILE_UTIL="0.6"
    COMPILE_STRATEGY="greedy"
    CUT_DESC="10 outputs (cut_onnx_small) — yolo26s"
fi

echo ""
echo "=================================================="
echo "FULL PIPELINE - best.pt -> HEF"
echo "Training:     ${TRAIN_FOLDER}"
echo "Model:        ${MODEL_NAME}"
echo "Resolution:   ${INPUT_SIZE}x${INPUT_SIZE}"
echo "Cut:          ${CUT_DESC}"
echo "Quantization: ${QUANT_MODE}"
echo "Compilation:  strategy=${COMPILE_STRATEGY}, max_utilization=${COMPILE_UTIL}"
echo "best.pt:      ${BEST_PT}"
echo "=================================================="

# --- Ensure container is running ---
echo ""
echo "Checking container..."
if ! sudo docker ps --format '{{.Names}}' | grep -q "${CONTAINER_NAME}"; then
    if sudo docker ps -a --format '{{.Names}}' | grep -q "${CONTAINER_NAME}"; then
        echo "Container stopped. Starting..."
        sudo docker start "${CONTAINER_NAME}"
    else
        echo "Container does not exist. Creating from image ${DOCKER_IMAGE_NAME}..."
        sudo docker run -d --name "${CONTAINER_NAME}" \
            --runtime=nvidia --gpus all \
            --net=host --privileged \
            -v "${SHARED_DIR}:/local/shared_with_docker:rw" \
            "${DOCKER_IMAGE_NAME}" sleep infinity
    fi
    sleep 3
fi
echo "Container OK."

# --- Step 0: Export ONNX (on host) ---
echo ""
echo "[0/4] Exporting ONNX (opset=17, imgsz=${INPUT_SIZE})..."
# shellcheck source=/dev/null
source "${HAILO_ENV}"
cd "${RUNS_BASE}/${TRAIN_FOLDER}/weights"
yolo export model=best.pt format=onnx simplify=true imgsz="${INPUT_SIZE}" opset=17

echo ""
echo "Copying ONNX to shared_with_docker..."
sudo cp "${RUNS_BASE}/${TRAIN_FOLDER}/weights/best.onnx" "${SHARED_DIR}/best.onnx"

# --- Step 1: ONNX cut ---
echo ""
if [ "${CUT_MODE}" = "3outputs" ]; then
    echo "[1/4] Cutting ONNX (3 outputs: bbox + score + mask_coef + proto)..."
    sudo docker exec -t "${CONTAINER_NAME}" bash /local/shared_with_docker/scripts/cut_onnx_nano.sh "${INPUT_SIZE}"
else
    echo "[1/4] Cutting ONNX (10 outputs: cv2/cv3/cv4 per scale + proto)..."
    sudo docker exec -t "${CONTAINER_NAME}" bash /local/shared_with_docker/scripts/cut_onnx_small.sh "${INPUT_SIZE}"
fi

# --- Step 2: Translate ONNX -> HAR ---
echo ""
echo "[2/4] Translating ONNX -> HAR..."
sudo docker exec -t "${CONTAINER_NAME}" bash /local/shared_with_docker/scripts/translate.sh "${MODEL_NAME}" "${INPUT_SIZE}"

# --- Step 3: INT8 quantization ---
echo ""
echo "[3/4] Quantizing (mode: ${QUANT_MODE})..."
if [ "${QUANT_MODE}" = "gpu" ]; then
    sudo docker exec -t \
        -e LD_LIBRARY_PATH=/usr/local/cuda-12.3/lib64:/usr/local/nvidia/lib:/usr/local/nvidia/lib64 \
        -e TF_ENABLE_ONEDNN_OPTS=0 \
        "${CONTAINER_NAME}" bash /local/shared_with_docker/scripts/quantize.sh "${MODEL_NAME}" "${INPUT_SIZE}" gpu
else
    sudo docker exec -t -e CUDA_VISIBLE_DEVICES= "${CONTAINER_NAME}" \
        bash /local/shared_with_docker/scripts/quantize.sh "${MODEL_NAME}" "${INPUT_SIZE}" "${QUANT_MODE}"
fi

# --- Step 4: Compile HAR -> HEF ---
echo ""
echo "[4/4] Compiling HAR -> HEF..."
sudo docker exec -t "${CONTAINER_NAME}" \
    bash /local/shared_with_docker/scripts/compile_hef.sh "${MODEL_NAME}" "${COMPILE_UTIL}" "${COMPILE_STRATEGY}"

echo ""
echo "=================================================="
echo "DONE: ${SHARED_DIR}/${MODEL_NAME}.hef"
echo "=================================================="
echo ""
echo "Next steps:"
echo "  1. Copy HEF to RPi5:"
echo "     scp \"${SHARED_DIR}/${MODEL_NAME}.hef\" \"${RPI5_HOST}:~/\""
echo "  2. Test on RPi5:"
echo "     python3 test_yolo26_hailo3.py camera ${MODEL_NAME}.hef"
echo "=================================================="
