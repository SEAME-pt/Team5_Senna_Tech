#!/bin/bash

RASP_USER="root"
RASP_IP="10.21.220.158"
RASP_DEST="/home/pipeline_jose"
PIPELINE_DIR="pipeline"

# Colors
GREEN='\033[0;32m'
RED='\033[0;31m'
NC='\033[0m'

# Check if pipeline dir exists
if [ ! -d "$PIPELINE_DIR" ]; then
    echo -e "${RED}Error: directory '$PIPELINE_DIR' not found.${NC}"
    exit 1
fi

echo "Syncing pipeline to $RASP_USER@$RASP_IP:$RASP_DEST"
echo "------------------------------------------------------"

rsync -avz \
    --include='*/' \
    --include='*.py' \
    --exclude='*' \
    "$PIPELINE_DIR/" \
    "$RASP_USER@$RASP_IP:$RASP_DEST/"

if [ $? -eq 0 ]; then
    echo -e "${GREEN}Sync completed successfully.${NC}"
else
    echo -e "${RED}Sync failed.${NC}"
fi
