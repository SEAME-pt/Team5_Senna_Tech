#!/bin/bash
output=$(../a.out -50)

if echo "$output" | grep -q "Speed OK"; then
    echo "A3.1: PASS" >> ../tsf/evidence.log
else
    echo "A3.1: FAIL" >> ../tsf/evidence.log
fi
