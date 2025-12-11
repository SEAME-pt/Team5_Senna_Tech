#!/bin/bash
# run_cppcheck.sh

# Sai se qualquer comando falhar
set -e

# Rodar cppcheck
cppcheck --enable=all \
        --suppress=unknownMacro \
         -isrc/CAN_communication \
         -isrc/threadx \
         -isrc/car_cluster/build \
         src/

echo "Cppcheck lint success."