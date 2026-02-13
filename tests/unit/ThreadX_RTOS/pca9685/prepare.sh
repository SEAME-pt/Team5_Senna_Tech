#!/bin/bash
set -e

GREEN="\033[0;32m"
NC="\033[0m"

# pega o diretório real onde o script está
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

EXPECTED_SUFFIX="tests/unit/ThreadX_RTOS/pca9685"

# valida path
if [[ "$SCRIPT_DIR" != *"$EXPECTED_SUFFIX" ]]; then
    echo "❌ Safety check failed!"
    echo "This script must run inside tests/unit/ThreadX_RTOS/pca9685"
    echo "Current path: $SCRIPT_DIR"
    exit 1
fi  

SRC_DIR="$SCRIPT_DIR/src"

# proteção extra: garantir que existe e não é vazio
if [[ ! -d "$SRC_DIR" || "$SRC_DIR" == "/" ]]; then
    echo "❌ Invalid src directory"
    exit 1
fi

rm -rf "$SRC_DIR"/*

cp "$SCRIPT_DIR/../../../../src/threadx/SennaTech/Core/Src/"{pca9685.c,car.c} "$SRC_DIR/"
cp "$SCRIPT_DIR/../../../../src/threadx/SennaTech/Core/Inc/"{pca9685.h,car.h,i2c_hal.h,sleep_hal.h} "$SRC_DIR/"

echo -e "${GREEN}ThreadX project files successfully copied. Ready to start unit test!${NC}"

