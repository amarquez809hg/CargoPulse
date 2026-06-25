#!/usr/bin/env bash
# Local Docker dev: live code mount + Django runserver
set -euo pipefail
cd "$(dirname "$0")"

if [[ ! -f .env ]]; then
  cp .env.example .env
fi

docker compose -f docker-compose.yml -f docker-compose.dev.yml up --build "$@"
