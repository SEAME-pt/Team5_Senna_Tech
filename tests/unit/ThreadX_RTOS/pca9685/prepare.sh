#!/bin/bash
set -e

GREEN="\033[0;32m"
NC="\033[0m"

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

EXPECTED_SUFFIX="tests/unit/ThreadX_RTOS/pca9685"

if [[ "$SCRIPT_DIR" != *"$EXPECTED_SUFFIX" ]]; then
    echo "❌ Safety check failed!"
    exit 1
fi

SRC_DIR="$SCRIPT_DIR/src"
SOURCE_ROOT="$SCRIPT_DIR/../../../../src/threadx/SennaTech"

if [[ ! -d "$SRC_DIR" || "$SRC_DIR" == "/" ]]; then
    echo "❌ Invalid src directory"
    exit 1
fi

rm -rf "$SRC_DIR"/*

find "$SOURCE_ROOT" -type f \( \
    -name "*.h" -o \
    -name "car.c" \
\) -exec cp {} "$SRC_DIR/" \;

echo -e "${GREEN}ThreadX project files successfully copied. Ready to start unit test!!${NC}"

