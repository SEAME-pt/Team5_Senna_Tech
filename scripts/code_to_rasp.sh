#!/bin/bash

RASP_USER="root"
RASP_IP="10.21.220.158"
RASP_DEST="/home/pipeline_robotaxi"
PIPELINE_DIR="Taxi_Robot"

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" >/dev/null 2>&1 && pwd)"
REPO_ROOT="$SCRIPT_DIR/.."
SOURCE_DIR="$REPO_ROOT/$PIPELINE_DIR"

if [ ! -d "$SOURCE_DIR" ] && [ -d "$REPO_ROOT/ADAS/$PIPELINE_DIR" ]; then
    SOURCE_DIR="$REPO_ROOT/ADAS/$PIPELINE_DIR"
fi

# Colors
GREEN='\033[0;32m'
RED='\033[0;31m'
NC='\033[0m'

# Check if pipeline dir exists
if [ ! -d "$SOURCE_DIR" ]; then
    echo -e "${RED}Error: directory '$SOURCE_DIR' not found.${NC}"
    exit 1
fi

echo "Syncing pipeline contents to $RASP_USER@$RASP_IP:$RASP_DEST/"
echo "------------------------------------------------------"

rsync -avz \
    "$SOURCE_DIR/" \
    "$RASP_USER@$RASP_IP:$RASP_DEST/"

if [ $? -eq 0 ]; then
    echo -e "${GREEN}Sync completed successfully.${NC}"
else
    echo -e "${RED}Sync failed.${NC}"
fi