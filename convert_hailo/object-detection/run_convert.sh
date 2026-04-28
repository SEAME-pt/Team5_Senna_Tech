#!/bin/bash

# ==============================================================================
# HAILO ULTIMATE ORCHESTRATOR - SENNA EDITION 🏁 (RAW OUTPUT / SOFTWARE NMS)
# YOLO26 OBJECT DETECTION PIPELINE
# ==============================================================================

# --- [COLOR DEFINITIONS] ---
RED='\033[0;31m'
WHITE='\033[1;37m'
YELLOW='\033[1;33m'
GREEN='\033[0;32m'
BLUE='\033[0;34m'
NC='\033[0m'

# --- [PATH CONFIGURATION] ---
DIR_CONVERSION="$(cd "$(dirname "$0")" && pwd)"
DIR_ROOT="$(cd "${DIR_CONVERSION}/.." && pwd)"

if [ -f "${DIR_ROOT}/.env.hailo.object" ]; then
    . "${DIR_ROOT}/.env.hailo.object"
fi

PROJECT_BASE="${BASE_PROJECT:-${HOME}/ADAS/Object-Detection}"
VENV_NAME="${VENV_NAME:-${DIR_ROOT}/hailo-env}"
CONTAINER_NAME="${CONTAINER_NAME:-hailo8_ai_sw_suite_2025-10_container}"
SHARED_DIR="${SHARED_DIR:-${DIR_ROOT}/shared_with_docker}"

# --- [VISUAL UTILITIES] ---
loading_animation() {
    local pid=$!
    local delay=0.1
    local spin='|/-\'
    while [ -d /proc/$pid ]; do
        local temp=${spin#?}
        printf " ${YELLOW}[%c]${NC}  " "$spin"
        local spin=$temp${spin%"$temp"}
        sleep $delay
        printf "\b\b\b\b\b\b"
    done
    printf "    \b\b\b\b"
}

# --- [START FLOW] ---
clear
echo -e "${RED}================================================================================"
echo -e "${WHITE}        HAILO ULTIMATE ORCHESTRATOR - YOLO26 DETECTION PIPELINE 🏁"
echo -e "${RED}================================================================================"
echo -e "${WHITE}PROJECT:${NC} $PROJECT_BASE"
echo -e "${WHITE}SHARED FOLDER:${NC} $SHARED_DIR"
echo -e "--------------------------------------------------------------------------------"

# --- [YOLO26 TRAINING VERSION SELECTION] ---
TRAININGS_DIR="${PROJECT_BASE}/trainings"

echo -e "\n${YELLOW}>> Select YOLO26 training version:${NC}"

# List available folders
mapfile -t TRAINING_LIST < <(ls -1 "$TRAININGS_DIR")

if [ ${#TRAINING_LIST[@]} -eq 0 ]; then
    echo -e "${RED}[ERROR] No training folders found in $TRAININGS_DIR${NC}"
    exit 1
fi

# Print options
for i in "${!TRAINING_LIST[@]}"; do
    echo "  $((i+1))) ${TRAINING_LIST[$i]}"
done

# Read selection
read -p "Choose version [1-${#TRAINING_LIST[@]}]: " SELECTED_INDEX

# Validate input
if ! [[ "$SELECTED_INDEX" =~ ^[0-9]+$ ]] || \
   [ "$SELECTED_INDEX" -lt 1 ] || \
   [ "$SELECTED_INDEX" -gt "${#TRAINING_LIST[@]}" ]; then
    echo -e "${RED}[ERROR] Invalid selection${NC}"
    exit 1
fi

SELECTED_VERSION="${TRAINING_LIST[$((SELECTED_INDEX-1))]}"

echo -e "${GREEN}Selected:${NC} $SELECTED_VERSION"

# --- MODEL PATH ---
MODEL_BASE="yolo26n"
MODEL_PT="${TRAININGS_DIR}/${SELECTED_VERSION}/weights/best.pt"

# --- [STEP 0: VALIDATION & CLEANUP] ---
echo -e "\n${RED}[STEP 0]${WHITE} VALIDATION${NC}"
echo -e "Target Model: ${BLUE}${MODEL_BASE}${NC}"

if [ ! -f "$MODEL_PT" ]; then 
    echo -e "${RED}[ERROR] Model file not found at: $MODEL_PT${NC}"
    exit 1
fi

if [ ! -d "$VENV_NAME" ]; then 
    echo -e "${RED}[ERROR] VENV not found at: $VENV_NAME${NC}"
    exit 1
fi

mkdir -p "$SHARED_DIR/calibration_images"
mkdir -p "$SHARED_DIR/scripts"

find "$SHARED_DIR" -mindepth 1 -maxdepth 1 ! -name "calibration_images" ! -name "scripts" -delete
rm -rf "$SHARED_DIR/calibration_images"/*
rm -rf "$SHARED_DIR/scripts"/*

chmod -R 777 "$SHARED_DIR"
echo -e "${GREEN}[OK] Environment prepared and shared folder cleaned${NC}"

# --- [STEP 0.1: PARAM EXTRACTION] ---
ARGS_YAML="$(dirname "$(dirname "$MODEL_PT")")/args.yaml"

echo -e "\n${YELLOW}[INFO] Extracting training parameters...${NC}"

if [ -f "$ARGS_YAML" ]; then
    TRAIN_IMGSZ=$(grep "^imgsz:" "$ARGS_YAML" | awk '{print $2}' | tr -d '[]' | cut -d',' -f1)
    TRAIN_CONF=$(grep "^conf:" "$ARGS_YAML" | awk '{print $2}' | head -n1)
    TRAIN_IOU=$(grep "^iou:" "$ARGS_YAML" | awk '{print $2}' | head -n1)

    [[ -z "$TRAIN_IMGSZ" ]] && TRAIN_IMGSZ=640
    [[ -z "$TRAIN_CONF" ]] && TRAIN_CONF=0.25
    [[ -z "$TRAIN_IOU" ]] && TRAIN_IOU=0.45

    echo -e "  Resolution: ${GREEN}${TRAIN_IMGSZ}${NC}"
    echo -e "  Confidence: ${GREEN}${TRAIN_CONF}${NC}"
    echo -e "  IoU:        ${GREEN}${TRAIN_IOU}${NC}"
else
    echo -e "${YELLOW}[WARNING] args.yaml not found. Using defaults.${NC}"
    TRAIN_IMGSZ=640; TRAIN_CONF=0.25; TRAIN_IOU=0.45
fi

# --- [STEP 1: ONNX EXPORT] ---
echo -e "\n${RED}[STEP 1]${WHITE} ONNX EXPORT${NC}"

source hailo-env/bin/activate
rm -f /tmp/yolo_export.log

printf "Exporting (${TRAIN_IMGSZ})... "
yolo export model="${MODEL_PT}" format=onnx simplify=true imgsz=${TRAIN_IMGSZ} opset=17 > /tmp/yolo_export.log 2>&1 &
loading_animation
wait $!

ONNX_FILE="$(dirname "$MODEL_PT")/best.onnx"

if [ -f "$ONNX_FILE" ]; then
    mv "$ONNX_FILE" "$SHARED_DIR/best.onnx"
    echo -e "${GREEN}[OK] ONNX model generated${NC}"
else
    echo -e "${RED}[ERROR] Export failed. Check /tmp/yolo_export.log${NC}"
    exit 1
fi

deactivate

# --- [STEP 2: CALIBRATION DATA] ---
echo -e "\n${RED}[STEP 2]${WHITE} CALIBRATION DATA${NC}"

find "$DATASETS_DIR" -type f \( -iname "*.jpg" -o -iname "*.png" \) \
| shuf | head -n "$NUM_CALIB_IMAGES" \
| while read -r img; do
    cp "$img" "$SHARED_DIR/calibration_images/"
done

echo -e "${GREEN}[OK] Calibration images ready${NC}"


# --- [STEP 3: DOCKER COMPILATION - INLINE] ---
echo -e "\n${RED}[STEP 3]${WHITE} HEF COMPILATION${NC}"

read -p "Start compilation? (y/n): " START

if [[ "$START" =~ ^[Yy]$ ]]; then
    STATUS=$(sudo docker inspect -f "{{.State.Status}}" "${CONTAINER_NAME}" 2>/dev/null)

    if [ "$STATUS" != "running" ]; then
        echo -e "${YELLOW}[WARNING] Container not running. Starting...${NC}"
        sudo docker start "${CONTAINER_NAME}" > /dev/null
    fi

    echo -e "${WHITE}Running compilation inside container...${NC}"

    sudo docker exec -i "$CONTAINER_NAME" /bin/bash <<EOF

# ================= INSIDE CONTAINER =================

MODEL_BASE="${MODEL_BASE}"
DIR_BASE="/local/shared_with_docker"
MODEL_ONNX="\${DIR_BASE}/best.onnx"
CALIB_PATH="\${DIR_BASE}/calibration_images"
HAILO_ARCH="hailo8"

WORKDIR="/tmp/hailo_compile"
rm -rf "\$WORKDIR" && mkdir -p "\$WORKDIR"
cd "\$WORKDIR"

echo "--------------------------------------------------"
echo "Starting HEF Compilation (Raw Output Mode)"
echo "Model: \$MODEL_BASE"
echo "ONNX:  \$MODEL_ONNX"
echo "Calib: \$CALIB_PATH"
echo "--------------------------------------------------"

if [ ! -f "\$MODEL_ONNX" ]; then
    echo "ERROR: ONNX model not found at \$MODEL_ONNX"
    exit 1
fi

cp "\$MODEL_ONNX" .

hailomz compile "\$MODEL_BASE" \
    --ckpt "./best.onnx" \
    --calib-path "\$CALIB_PATH" \
    --hw-arch "\$HAILO_ARCH"

if [ \$? -eq 0 ]; then
    echo "--------------------------------------------------"
    echo "Compilation SUCCESS. Moving outputs..."

    mv ./*.hef "\$DIR_BASE/" 2>/dev/null
    mv ./*.har "\$DIR_BASE/" 2>/dev/null

    echo "DONE - HEF generated:"
    ls -lh "\$DIR_BASE"/*.hef
    exit 0
else
    echo "--------------------------------------------------"
    echo "Compilation FAILED"
    exit 1
fi

# ===================================================

EOF

    if [ $? -eq 0 ]; then
        echo -e "\n${GREEN}========================================"
        echo -e " PIPELINE COMPLETED SUCCESSFULLY"
        echo -e "========================================${NC}"
        echo -e "Output: ${SHARED_DIR}"
    else
        echo -e "${RED}[ERROR] Compilation failed${NC}"
        exit 1
    fi
fi