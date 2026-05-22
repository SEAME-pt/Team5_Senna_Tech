#!/bin/bash

# ==============================================================================
# HAILO ULTIMATE ORCHESTRATOR - SENNA EDITION (RAW OUTPUT / SOFTWARE NMS)
# ==============================================================================

# --- [COLOR DEFINITIONS] ---
RED='\033[0;31m'
WHITE='\033[1;37m'
YELLOW='\033[1;33m'
GREEN='\033[0;32m'
BLUE='\033[0;34m'
NC='\033[0m'

# --- [PATH CONFIGURATION] ---
CONVERSION_DIR="$(cd "$(dirname "$0")" && pwd)"
ROOT_DIR="$(cd "${CONVERSION_DIR}/.." && pwd)"

if [ -f "${ROOT_DIR}/.env.hailo" ]; then
    . "${ROOT_DIR}/.env.hailo"
fi

PROJECT_BASE="${BASE_PROJECT:-${HOME}/Documents/ADAS/LKA_model}"
VENV_PATH="${VENV_NAME:-${ROOT_DIR}/hailo-env}"
CONTAINER_NAME_VALUE="${CONTAINER_NAME:-hailo8_ai_sw_suite_2025-10_container}"
SHARED_DIR_PATH="${SHARED_DIR:-${ROOT_DIR}/shared_with_docker}"

# --- [VISUAL HELPERS] ---
loading_animation() {
    local pid=$!
    local wait_time=0.1
    local characters='|/-\'
    while [ -d /proc/$pid ]; do
        local temp=${characters#?}
        printf " ${YELLOW}[%c]${NC}  " "$characters"
        local characters=$temp${characters%"$temp"}
        sleep $wait_time
        printf "\b\b\b\b\b\b"
    done
    printf "    \b\b\b\b"
}

# --- [FLOW START] ---
clear
echo -e "${RED}================================================================================"
echo -e "${WHITE}                HAILO ULTIMATE ORCHESTRATOR: SENNA EDITION (RAW OUTPUT)"
echo -e "${RED}================================================================================"
echo -e "${WHITE}PROJECT:${NC} $PROJECT_BASE"
echo -e "${WHITE}SHARED FOLDER:${NC} $SHARED_DIR_PATH"
echo -e "--------------------------------------------------------------------------------"

# --- [INTERACTIVE STEP] ---
echo -e "${YELLOW}>> Select the training run:${NC}"
echo -n "Folder name: "
read RUN_INPUT
RUN_NAME="${RUN_INPUT}"

if [ -z "$RUN_NAME" ]; then
    echo -e "${RED}[ERROR] Training run name is required.${NC}"
    exit 1
fi

# --- [MODEL SELECTION STEP] ---
echo -e "\n${YELLOW}>> Select the YOLOv8-seg model scale:${NC}"
echo -e "  1 or n) Nano   (yolov8n_seg)"
echo -e "  2 or s) Small  (yolov8s_seg)"
echo -e "  3 or m) Medium (yolov8m_seg)"
echo -e "  4 or l) Large  (yolov8l_seg)"
echo -e "  5 or x) XLarge (yolov8x_seg)"
read -p "Choice [Default 1/n]: " MODEL_CHOICE

# Convert to lowercase to simplify comparisons
MODEL_CHOICE=$(echo "$MODEL_CHOICE" | tr '[:upper:]' '[:lower:]')

case $MODEL_CHOICE in
    2|s) MODEL_BASE="yolov8s_seg" ;;
    3|m) MODEL_BASE="yolov8m_seg" ;;
    4|l) MODEL_BASE="yolov8l_seg" ;;
    5|x) MODEL_BASE="yolov8x_seg" ;;
    1|n|"") MODEL_BASE="yolov8n_seg" ;;
    *) 
        echo -e "${YELLOW}[WARNING] Invalid choice. Using Nano (yolov8n_seg) by default.${NC}"
        MODEL_BASE="yolov8n_seg" 
        ;;
esac

MODEL_PT="${PROJECT_BASE}/runs/${RUN_NAME}/weights/best.pt"
DATASETS_DIR="${PROJECT_BASE}/datasets"
NUM_CALIB_IMAGES=1024

# --- [STEP 0: VALIDATION AND CLEANUP] ---
echo -e "\n${RED}[STEP 0]${WHITE} SEARCHING FOR THE IDEAL SETUP (VALIDATION)${NC}"
echo -e "Target model: ${BLUE}${MODEL_BASE}${NC}"

if [ ! -f "$MODEL_PT" ]; then 
    echo -e "${RED}[ERROR] Model file not found at: $MODEL_PT${NC}"
    exit 1
fi

if [ ! -d "$VENV_PATH" ]; then 
    echo -e "${RED}[ERROR] Virtual environment not found at: $VENV_PATH${NC}"
    exit 1
fi

mkdir -p "$SHARED_DIR_PATH/calibration_images"
mkdir -p "$SHARED_DIR_PATH/scripts"
find "$SHARED_DIR_PATH" -mindepth 1 -maxdepth 1 ! -name "calibration_images" ! -name "scripts" ! -name "README.md" -delete
rm -rf "$SHARED_DIR_PATH/calibration_images"/*
rm -rf "$SHARED_DIR_PATH/scripts"/*

chmod -R 777 "$SHARED_DIR_PATH"
echo -e "${GREEN}  [OK] - Environment prepared and shared folder cleaned (permissions 777)${NC}"

# --- [STEP 0.1: PARAMETER EXTRACTION] ---
ARGS_YAML="$(dirname "$(dirname "$MODEL_PT")")/args.yaml"
echo -e "\n${YELLOW}[INFO] Extracting original training parameters...${NC}"

if [ -f "$ARGS_YAML" ]; then
    TRAIN_IMGSZ=$(grep "^imgsz:" "$ARGS_YAML" | awk '{print $2}' | tr -d '[]' | cut -d',' -f1)
    TRAIN_CONF=$(grep "^conf:" "$ARGS_YAML" | awk '{print $2}' | head -n1)
    TRAIN_IOU=$(grep "^iou:" "$ARGS_YAML" | awk '{print $2}' | head -n1)
    NUM_CLASSES=$(grep "^nc:" "$ARGS_YAML" | awk '{print $2}' || echo 1)
    
    [[ -z "$TRAIN_IMGSZ" || "$TRAIN_IMGSZ" == "null" ]] && TRAIN_IMGSZ=640
    [[ -z "$TRAIN_CONF" || "$TRAIN_CONF" == "null" ]] && TRAIN_CONF=0.25
    [[ -z "$TRAIN_IOU" || "$TRAIN_IOU" == "null" ]] && TRAIN_IOU=0.45
    [[ -z "$NUM_CLASSES" || "$NUM_CLASSES" == "null" ]] && NUM_CLASSES=1
    
    echo -e "  - Detected resolution: ${GREEN}${TRAIN_IMGSZ}x${TRAIN_IMGSZ}${NC}"
    echo -e "  - Confidence (threshold): ${GREEN}${TRAIN_CONF}${NC}"
    echo -e "  - IoU (NMS): ${GREEN}${TRAIN_IOU}${NC}"
    echo -e "  - Number of classes: ${GREEN}${NUM_CLASSES}${NC}"
else
    echo -e "  ${YELLOW}[WARNING] args.yaml not found. Using defaults.${NC}"
    TRAIN_IMGSZ=640; TRAIN_CONF=0.25; TRAIN_IOU=0.45; NUM_CLASSES=1
fi

# --- [STEP 1: ONNX EXPORT] ---
echo -e "\n${RED}[STEP 1]${WHITE} CHANGING THE TIRES (ONNX EXPORT)${NC}"
echo -e "  Model path: ${BLUE}${MODEL_PT}${NC}"

source "$VENV_PATH/bin/activate"
rm -f /tmp/yolo_export.log

printf "  Running export (${TRAIN_IMGSZ}x${TRAIN_IMGSZ})... "
yolo export model="${MODEL_PT}" format=onnx simplify=true imgsz=${TRAIN_IMGSZ} opset=12 > /tmp/yolo_export.log 2>&1 &
loading_animation
wait $!

GENERATED_ONNX="$(dirname "$MODEL_PT")/best.onnx"
if [ -f "$GENERATED_ONNX" ]; then
    mv "$GENERATED_ONNX" "$SHARED_DIR_PATH/best.onnx"
    echo -e "${GREEN}  [OK] - ONNX model generated and moved${NC}"
else
    echo -e "${RED}  [ERROR] Export failed. Check /tmp/yolo_export.log${NC}"
    exit 1
fi

# --- [STEP 2: CALIBRATION PREPARATION] ---
echo -e "\n${RED}[STEP 2]${WHITE} TRACK STRATEGY (INT8 CALIBRATION)${NC}"
printf "  Collecting $NUM_CALIB_IMAGES images... "
counter=1
find "$DATASETS_DIR" -type f \( -iname "*.jpg" -o -iname "*.jpeg" -o -iname "*.png" \) | shuf | head -n "$NUM_CALIB_IMAGES" | while read -r img; do
    extension="${img##*.}"
    cp "$img" "$SHARED_DIR_PATH/calibration_images/calib_${counter}.${extension}"
    counter=$((counter + 1))
done
echo -e "${GREEN}DONE${NC}"
echo -e "${GREEN}  [OK] - $(find "$SHARED_DIR_PATH/calibration_images" -type f | wc -l) images ready for calibration${NC}"

# --- [STEP 2.1: NMS CONFIGURATION GENERATION (TAPPAS)] ---
echo -e "\n${RED}[STEP 2.1]${WHITE} BOX SYNCHRONIZATION (NMS CONFIG)${NC}"
echo -e "${YELLOW}[INFO] Generating a custom nms_config.json file for Tappas...${NC}"

cat <<EOF > "$SHARED_DIR_PATH/nms_config.json"
{
    "nms_scores_th": ${TRAIN_CONF},
    "nms_iou_th": ${TRAIN_IOU},
    "max_proposals_per_class": 100,
    "classes": ${NUM_CLASSES},
    "background_removal": false,
    "meta_arch": "yolov8"
}
EOF

echo -e "${GREEN}  [OK] - nms_config.json generated successfully in the shared folder${NC}"

# Restore compilation scripts
cp "${CONVERSION_DIR}/scripts/compile.sh" "$SHARED_DIR_PATH/scripts/compile.sh"
chmod +x "$SHARED_DIR_PATH/scripts/compile.sh"
echo -e "${GREEN}  [OK] - Specialist compile.sh script restored (raw output mode)${NC}"
deactivate

# --- [STEP 3: DOCKER COMPILATION] ---
echo -e "\n${RED}[STEP 3]${WHITE} CHECKERED FLAG (HEF COMPILATION)${NC}"
echo -e "${YELLOW}>> Start official compilation (Hailo Model Zoo) for ${MODEL_BASE}? (y/n)${NC}"
read START_COMPILATION

if [[ "$START_COMPILATION" =~ ^[YySs]$ ]]; then
    STATUS=$(sudo docker inspect -f "{{.State.Status}}" "${CONTAINER_NAME_VALUE}" 2>/dev/null)
    
    if [ "$STATUS" != "running" ]; then
        echo -e "${YELLOW}  [WARNING] Container is not running. Starting it...${NC}"
        sudo docker start "${CONTAINER_NAME_VALUE}" > /dev/null
    fi

    echo -e "${WHITE}  Running compilation (raw output mode)...${NC}"
    if sudo docker exec -it "$CONTAINER_NAME_VALUE" /bin/bash -c "/local/shared_with_docker/scripts/compile.sh ${MODEL_BASE}"; then
        echo -e "\n${RED}================================================================================"
        echo -e "${GREEN}                        SUCCESS! PROCESS COMPLETED."
        echo -e "${RED}================================================================================"
        echo -e "${WHITE}The binary (.hef) is available at:${NC} $SHARED_DIR_PATH/"
        echo -e "--------------------------------------------------------------------------------"
        echo -e "${YELLOW}POST-PROCESSING STRATEGY (SOFTWARE NMS):${NC}"
        echo -e "  - Model scale:          ${GREEN}${MODEL_BASE}${NC}"
        echo -e "  - Training parameters:${NC}"
        echo -e "    - Confidence:         ${GREEN}${TRAIN_CONF}${NC}"
        echo -e "    - IoU (NMS):          ${GREEN}${TRAIN_IOU}${NC}"
        echo -e "    - Number of classes:  ${GREEN}${NUM_CLASSES}${NC}"
        echo -e "  - Tappas configuration: ${GREEN}nms_config.json generated${NC}"
        echo -e "--------------------------------------------------------------------------------"
    else
        echo -e "${RED}\n  [ERROR] Compilation failed.${NC}"
        exit 1
    fi
fi
