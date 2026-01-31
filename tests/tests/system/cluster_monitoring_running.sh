#!/bin/bash

# Pega a última vez que o serviço system_monitor.service foi ativado
LAST_RUN=$(systemctl show -p ExecMainStartTimestamp system_monitor.service | cut -d= -f2)

if [ -z "$LAST_RUN" ]; then
    echo "Timer has never run."
    exit 1
fi

# Converte para timestamp em segundos desde Epoch
LAST_TS=$(date -d "$LAST_RUN" +%s)
NOW_TS=$(date +%s)

# Limite em segundos (quanto tempo atrás consideramos válido)
LIMIT=20

# Comparação
DIFF=$(( NOW_TS - LAST_TS ))

echo "Last run: $LAST_RUN ($DIFF seconds ago)"

tail -n 3 /var/log/system.txt 

# Se o timer rodou nos últimos $LIMIT segundos, exit 0, senão exit 1
if [ "$DIFF" -le "$LIMIT" ]; then
    exit 0
else
    exit 1
fi