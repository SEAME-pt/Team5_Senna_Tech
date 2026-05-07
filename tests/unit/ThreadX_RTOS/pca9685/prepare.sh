#!/bin/bash
set -eux

GREEN="\033[0;32m"
NC="\033[0m"

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

EXPECTED_SUFFIX="tests/unit/ThreadX_RTOS/pca9685"

if [[ "$SCRIPT_DIR" != *"$EXPECTED_SUFFIX" ]]; then
    echo "❌ Safety check failed!"
    echo "This script must run inside tests/unit/ThreadX_RTOS/pca9685"
    echo "Current path: $SCRIPT_DIR"
    exit 1
fi

SRC_DIR="$SCRIPT_DIR/src"
INC_DIR="$SCRIPT_DIR/inc"

if [[ ! -d "$SRC_DIR" || "$SRC_DIR" == "/" ]]; then
    echo "❌ Invalid src directory"
    exit 1
fi

mkdir -p "$SRC_DIR"
mkdir -p "$INC_DIR"

rm -rf "$SRC_DIR"/*
rm -rf "$INC_DIR"/*

cp -rf "$SCRIPT_DIR/../../../../src/threadx/SennaTech/Core/Src/." "$SRC_DIR/"
cp -rf "$SCRIPT_DIR/../../../../src/threadx/SennaTech/Core/Inc/." "$INC_DIR/"

echo -e "${GREEN}ThreadX project files successfully copied. Ready to start unit test!${NC}"

