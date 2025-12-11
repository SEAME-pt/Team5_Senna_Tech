#!/bin/bash
# run_cppcheck.sh

# Sai se qualquer comando falhar
set -e

# Rodar cppcheck
cppcheck --enable=style \
        --suppress=unknownMacro \
         -isrc/CAN_communication \
         -isrc/threadx \
         -isrc/car_cluster/build \
         --error-exitcode=1 \
         src/

echo "Cppcheck lint success."