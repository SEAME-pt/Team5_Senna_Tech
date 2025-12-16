#!/bin/bash
echo "--- TSF Evidence Report ---" > ../tsf/evidence.log
echo "Running tests..." >> ../tsf/evidence.log

chmod +x *.sh

for t in *.sh; do
    if [[ "$t" != "run_tests.sh" ]]; then
        bash "$t"
    fi
done

echo "Done. Evidence written to tsf/evidence.log"
