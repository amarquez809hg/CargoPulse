#!/usr/bin/env bash
# Compile Spanish translations (requires gettext: brew install gettext)
set -euo pipefail
cd "$(dirname "$0")/.."
python manage.py compilemessages -l es
echo "Translations compiled → locale/es/LC_MESSAGES/django.mo"
