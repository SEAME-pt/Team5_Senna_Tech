#!/bin/bash

SERVICE="check-update.service"

echo "Checking update service: $SERVICE"

# 1. Verifica se o service existe
if ! systemctl list-unit-files | grep -q "^$SERVICE"; then
    echo "Check Update service: FAIL"
    exit 1
fi

# 2. Verifica se está habilitado
ENABLED=$(systemctl is-enabled "$SERVICE" 2>/dev/null)

if [ "$ENABLED" != "enabled" ]; then
    echo "Check Update service: FAIL"
    exit 1
fi

# 3. Tenta iniciar o serviço
systemctl start "$SERVICE"
sleep 2

# 4. Verifica status
STATUS=$(systemctl is-active "$SERVICE")

if [ "$STATUS" != "active" ] && [ "$STATUS" != "inactive" ]; then
    echo "Check Update service: FAIL" 
    exit 1
fi

echo "OK: Update service exists, is enabled, and runs correctly"
exit 0
