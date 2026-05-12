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

# Find all .py files under pipeline/
FILES=$(find "$PIPELINE_DIR" -name "*.py")

if [ -z "$FILES" ]; then
    echo -e "${RED}No .py files found under '$PIPELINE_DIR'.${NC}"
    exit 1
fi

echo "Syncing .py files to $RASP_USER@$RASP_IP:$RASP_DEST"
echo "------------------------------------------------------"

SUCCESS=0
FAIL=0

for FILE in $FILES; do
    scp "$FILE" "$RASP_USER@$RASP_IP:$RASP_DEST" 2>/dev/null
    if [ $? -eq 0 ]; then
        echo -e "${GREEN}[OK]${NC}   $FILE"
        ((SUCCESS++))
    else
        echo -e "${RED}[FAIL]${NC} $FILE"
        ((FAIL++))
    fi
done

echo "------------------------------------------------------"
echo "Done: $SUCCESS sent, $FAIL failed."