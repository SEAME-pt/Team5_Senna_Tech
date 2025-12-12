#!/bin/bash
# run cpp_check.sh

# Exit if any command fail
set -e

cppcheck --enable=style,warning \
        --suppress=unknownMacro \
         -isrc/CAN_communication/CAN_speedsensor \
         -isrc/threadx \
         -isrc/car_cluster/build \
         --error-exitcode=1 \
         src/

echo "Cppcheck lint success."

