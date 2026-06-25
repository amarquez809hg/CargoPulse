#!/usr/bin/env bash
# Production stack: Postgres + Gunicorn on port 8000
set -euo pipefail
cd "$(dirname "$0")"

if [[ ! -f .env ]]; then
  cp .env.example .env
  echo "Created docker/.env from .env.example"
  echo "Edit SECRET_KEY and POSTGRES_PASSWORD before a public deploy."
fi

docker compose up --build -d "$@"
echo ""
echo "Cargo Pulse (Docker) → http://127.0.0.1:${WEB_PORT:-8000}/"
echo "Logs: docker compose logs -f web"
echo "Stop: docker compose down"
