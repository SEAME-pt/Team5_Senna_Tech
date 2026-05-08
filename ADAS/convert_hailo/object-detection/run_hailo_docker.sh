#!/bin/bash

# ==============================================================================
# HAILO DOCKER MANAGER - HYBRID VERSION (SNAP AUTO-DETECTION)
# ==============================================================================
# This script automatically detects whether Docker was installed via Snap
# and applies the required hardware and permission adjustments.

export LC_ALL=C # To get the expected output for a non-English systems
set -e

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"

if [ -f "${PROJECT_ROOT}/.env.hailo" ]; then
    . "${PROJECT_ROOT}/.env.hailo"
fi

RESUME_CONTAINER=false
OVERRIDE_CONTAINER=false

readonly CONTAINER_NAME="${CONTAINER_NAME:-hailo8_ai_sw_suite_2025-10_container}"
readonly XAUTH_FILE=/tmp/hailo_docker.xauth
readonly DOCKER_TAR_FILE="${DOCKER_TAR_FILE:-hailo8_ai_sw_suite_docker_2025-10.tar.gz}"
readonly DOCKER_IMAGE_NAME="${DOCKER_IMAGE_NAME:-hailo8_ai_sw_suite_2025-10:1}"
readonly NVIDIA_GPU_EXIST=$(lspci | grep -i "\(vga\|3d\|display\|video\|graphics\).*nvidia" || true)
readonly NVIDIA_DOCKER_EXIST=$(dpkg -l | grep 'nvidia-docker\|nvidia-container-toolkit' || true)
readonly SHARED_DIR="${SHARED_DIR:-${PROJECT_ROOT}/shared_with_docker}"
readonly DEFAULT_HAILORT_LOGGER_PATH="/var/log/hailo"

readonly WHITE="\e[0m"
readonly CYAN="\e[1;36m"
readonly RED="\e[1;31m"
readonly YELLOW="\e[0;33m"

# --- [ENVIRONMENT DETECTION] ---
function check_if_snap() {
    if snap list docker &>/dev/null || [[ $(which docker) == *"/snap/"* ]]; then
        return 0 # Snap installation
    else
        return 1 # Standard installation
    fi
}

# --- [ARGUMENT PREPARATION] ---
function prepare_docker_args() {
    # Base arguments shared by all installation types
    DOCKER_ARGS="--privileged \
                 --net=host \
                 -e DISPLAY=$DISPLAY \
                 -e XDG_RUNTIME_DIR=$XDG_RUNTIME_DIR \
                 --device=/dev/dri:/dev/dri \
                 --ipc=host \
                 -v /dev:/dev \
                 -v ${XAUTH_FILE}:/home/hailo/.Xauthority \
                 -v /tmp/.X11-unix/:/tmp/.X11-unix/ \
                 --name $CONTAINER_NAME \
                 -v /var/run/docker.sock:/var/run/docker.sock \
                 -v /etc/machine-id:/etc/machine-id:ro \
                 -v /var/run/dbus/system_bus_socket:/var/run/dbus/system_bus_socket \
                 -v ${SHARED_DIR}:/local/shared_with_docker:rw \
                 -v /etc/timezone:/etc/timezone:ro \
                 -v /etc/localtime:/etc/localtime:ro"

    # Conditional logic: SNAP vs STANDARD
    if check_if_snap; then
        echo -e "${YELLOW}INFO: Docker via SNAP detected. Applying isolation adjustments...${WHITE}"
        # On Docker Snap with NVIDIA GPU support, keep the container args lean.
        # The extra host driver mounts below can break the NVIDIA prestart hook
        # even when `--runtime=nvidia --gpus all` is otherwise working.
        local VIDEO_GID=$(getent group video | cut -d: -f3 || echo "44")
        DOCKER_ARGS+=" --group-add ${VIDEO_GID}"
    else
        echo -e "${CYAN}INFO: Standard Docker installation detected.${WHITE}"
        # In the standard setup, group 44 is typically enough for Hailo
        DOCKER_ARGS+=" --group-add 44"
    fi

    # NVIDIA GPU checks
    if [[ $NVIDIA_GPU_EXIST ]] && [[ $NVIDIA_DOCKER_EXIST ]]; then
        DOCKER_ARGS+=" --gpus all "
    fi
}

# --- [IMAGE MANAGEMENT] ---
function load_hailo_ai_sw_suite_image() {
    if [[ ! -f "${DOCKER_TAR_FILE}" ]]; then
        echo -e "${RED}ERROR: File ${DOCKER_TAR_FILE} not found at the project root.${WHITE}" && exit 1
    fi
    echo -e "${CYAN}Loading official Hailo image...${WHITE}"
    sudo docker load -i "${PROJECT_ROOT}/${DOCKER_TAR_FILE}"
}

# --- [EXECUTION FLOW] ---
function main() {
    mkdir -p "${SHARED_DIR}"
    chmod -R 777 "${SHARED_DIR}" 2>/dev/null || true
    
    # Prepare display permissions (X11)
    touch $XAUTH_FILE
    xauth nlist $DISPLAY | sed -e 's/^..../ffff/' | xauth -f $XAUTH_FILE nmerge - 2>/dev/null || true
    chmod o+rw $XAUTH_FILE 2>/dev/null || true

    # Check whether the container already exists
    NUM_EXIST=$(sudo docker ps -a -q -f "name=$CONTAINER_NAME" | wc -l)

    if [ "$NUM_EXIST" -ge "1" ]; then
        STATUS=$(sudo docker inspect -f "{{.State.Status}}" "${CONTAINER_NAME}")
        
        # If it is stuck in an error state (created but not running), remove it and recreate it
        if [ "$STATUS" == "created" ]; then
             echo -e "${YELLOW}Cleaning container stuck after mount failure...${WHITE}"
             sudo docker rm "$CONTAINER_NAME"
             NUM_EXIST=0
        fi
    fi

    if [ "$NUM_EXIST" -ge "1" ]; then
        STATUS=$(sudo docker inspect -f "{{.State.Status}}" "${CONTAINER_NAME}")
        echo -e "${CYAN}Resuming existing container (Status: $STATUS)${WHITE}"
        sudo docker start "$CONTAINER_NAME"
        sudo docker exec -it -e DISPLAY=$DISPLAY "$CONTAINER_NAME" /bin/bash
    else
        # If the image is not loaded yet, load it now
        if [ "$(sudo docker images -q $DOCKER_IMAGE_NAME 2> /dev/null)" == "" ]; then
            load_hailo_ai_sw_suite_image
        fi
        
        prepare_docker_args
        echo -e "${CYAN}Starting new container...${WHITE}"
        sudo docker run ${DOCKER_ARGS} -ti $DOCKER_IMAGE_NAME
    fi
}

main "$@"
