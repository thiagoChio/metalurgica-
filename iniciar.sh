#!/usr/bin/env bash
# Correa Metalúrgica — sobe o site em http://127.0.0.1:8000 (macOS / Linux)
set -e
cd "$(dirname "$0")"

if ! command -v python3 >/dev/null; then
  echo "[ERRO] Python 3 não encontrado. Instale em https://www.python.org/downloads/"
  exit 1
fi

if [ ! -x ".venv/bin/python" ]; then
  echo "Primeira execução: preparando o ambiente..."
  python3 -m venv .venv
  .venv/bin/python -m pip install --upgrade pip --quiet
  .venv/bin/python -m pip install -r requirements.txt --quiet
  echo "Ambiente pronto."
fi

echo "Abrindo http://127.0.0.1:8000 — Ctrl+C encerra."
( sleep 2; (command -v open >/dev/null && open http://127.0.0.1:8000) \
  || (command -v xdg-open >/dev/null && xdg-open http://127.0.0.1:8000) ) &
exec .venv/bin/python run.py
