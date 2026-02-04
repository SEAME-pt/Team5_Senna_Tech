#!/bin/bash

GREEN="\033[0;32m"

rm -rf src/*

cp ../../../../src/threadx/SennaTech/Core/Src/{pca9685.c,car.c} src/

cp ../../../../src/threadx/SennaTech/Core/Inc/{pca9685.h,car.h,i2c_hal.h,sleep_hal.h} src/

echo -e "${GREEN}ThreadX project files successfully copied. Ready to start unit test!${NC}"
