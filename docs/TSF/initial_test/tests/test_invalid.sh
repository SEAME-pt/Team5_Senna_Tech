#!/bin/bash
output1=$(../a.out -5)
output2=$(../a.out 200)

if echo "$output1" | grep -q "FAULT" && echo "$output2" | grep -q "FAULT"; then
    echo "A2.1: PASS" >> ../tsf/evidence.log
else
    echo "A2.1: FAIL" >> ../tsf/evidence.log
fi
