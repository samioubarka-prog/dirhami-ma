#!/bin/bash
set -e

echo "=== DIRHAMI STARTUP ==="
echo "Python: $(python --version)"
echo "Port: $PORT"

# Verifier que le dossier static existe
if [ ! -d "static" ]; then
    echo "ERROR: static/ directory not found"
    ls -la
    exit 1
fi

# Lancer uvicorn avec logs
cd /opt/render/project/src
exec uvicorn app.main:app --host 0.0.0.0 --port $PORT --log-level debug
