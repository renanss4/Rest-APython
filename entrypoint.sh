#!/bin/sh
set -e

# Garante que as variáveis PORT e HOST estejam definidas
: "${PORT:?Need to set PORT non-empty}"
: "${HOST:?Need to set HOST non-empty}"

# 1) Cria tabela(s) no banco (caso ainda não existam)
python create_db.py

# 2) Sobe o servidor Uvicorn
exec uvicorn main:app \
     --host "$HOST" \
     --port "$PORT"
