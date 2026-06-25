#!/usr/bin/env bash
set -euo pipefail

echo "Running database migrations..."
python manage.py migrate --noinput

echo "Compiling translations..."
python manage.py compilemessages -l es

echo "Collecting static files..."
python manage.py collectstatic --noinput

echo "Starting application: $*"
exec "$@"
