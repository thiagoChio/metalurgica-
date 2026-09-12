#!/usr/bin/env bash
# Modo apresentação: igual ao iniciar.sh, sem os lembretes de obra na tela.
set -e
cd "$(dirname "$0")"
export SITE_DEBUG=false
exec ./iniciar.sh
