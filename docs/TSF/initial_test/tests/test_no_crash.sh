#!/bin/bash
../a.out 100 > /dev/null 2>&1
if [ $? -eq 0 ]; then
    echo "A1.1: PASS" >> ../tsf/evidence.log
else
    echo "A1.1: FAIL" >> ../tsf/evidence.log
fi
