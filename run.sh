#!/usr/bin/env bash
# Start Cargo Pulse local dev server (venv, SQLite)
set -euo pipefail
cd "$(dirname "$0")"
source venv/bin/activate
python manage.py migrate --noinput
echo ""
echo "Cargo Pulse → http://127.0.0.1:8000/"
echo "Admin → http://127.0.0.1:8000/admin/  (run: python manage.py createsuperuser)"
echo ""
echo "Docker (Postgres + Gunicorn): cd docker && ./run.sh"
echo "Docker dev:                  cd docker && ./run-dev.sh"
echo ""
python manage.py runserver
