#!/bin/bash

BASE_DIR="$(cd "$(dirname "$0")" && pwd)"
LOG_DIR="$BASE_DIR/logs"
LOG_FILE="$LOG_DIR/system.log"

TESTS=(
    "cluster_auto_start.sh"
    "check_update_started.sh"
)

# Cria pasta de logs se não existir
mkdir -p "$LOG_DIR"

# Cria / limpa o arquivo de log
echo "=== System Test Run: $(date) ===" > "$LOG_FILE"

echo "Logs: $LOG_FILE"
echo

RESULT=0

for TEST in "${TESTS[@]}"; do
    TEST_PATH="$BASE_DIR/$TEST"

    if [ ! -x "$TEST_PATH" ]; then
        echo "[ERROR] Test not found or not executable: $TEST"
        echo "[ERROR] $TEST not found or not executable" >> "$LOG_FILE"
        RESULT=1
        continue
    fi

    echo "Running test: $TEST"
    echo "--- Running $TEST ---" >> "$LOG_FILE"

    # Executa o teste e captura saída
    OUTPUT=$("$TEST_PATH" 2>&1)
    EXIT_CODE=$?

    echo "$OUTPUT" | tee -a "$LOG_FILE"

    if [ $EXIT_CODE -eq 0 ]; then
        echo "[PASS] $TEST" | tee -a "$LOG_FILE"
    else
        echo "[FAIL] $TEST" | tee -a "$LOG_FILE"
        RESULT=1
    fi

    echo >> "$LOG_FILE"
done

echo "=== Test Run Finished: $(date) ===" >> "$LOG_FILE"

if [ $RESULT -eq 0 ]; then
    echo "ALL TESTS PASSED"
else
    echo "SOME TESTS FAILED"
fi

exit $RESULT
