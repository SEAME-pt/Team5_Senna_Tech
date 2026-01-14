#!/bin/bash

LOG_FILE="/var/log/system.txt"
DATE=$(date "+%Y-%m-%d %H:%M:%S")

# Temperatura da CPU
TEMP_RAW=$(cat /sys/class/thermal/thermal_zone0/temp)
TEMP_C=$(echo "scale=1; $TEMP_RAW / 1000" | bc)

# Memória RAM em porcentagem
MEM_TOTAL=$(free -m | awk '/Mem:/ {print $2}')
MEM_USED=$(free -m | awk '/Mem:/ {print $3}')
MEM_USAGE_PERCENT=$(( MEM_USED * 100 / MEM_TOTAL ))

# Salvar no log
{
    echo "$DATE"
    echo "TEMP=${TEMP_C}"
    echo "MEMORY_USAGE=${MEM_USAGE_PERCENT}%"
} >> "$LOG_FILE"