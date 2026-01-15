#!/bin/bash

# Pega a primeira linha do log do cluster
LINE=$(journalctl -b -t cluster-start -o short-monotonic | head -n1)

if [ -z "$LINE" ]; then
    exit 1
fi

# Extrai o número entre colchetes
START_TIME=$(echo "$LINE" | sed -E 's/^\[\s*([0-9]+\.[0-9]+)\].*$/\1/')

LIMIT=15

# Comparação float
echo "Cluster started: $START_TIME after boot."
awk -v t="$START_TIME" -v l="$LIMIT" 'BEGIN { if (t <= l) { exit 0 } else { exit 1 } }'
exit $?
