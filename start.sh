#!/bin/bash
set -e

echo "ALLOWED_HOSTS=$ALLOWED_HOSTS"
echo "RENDER_EXTERNAL_HOSTNAME=$RENDER_EXTERNAL_HOSTNAME"
echo "Running migrations..."
python manage.py migrate --noinput

# Create superuser from env vars if set and user doesn't exist yet.
if [ -n "$DJANGO_SUPERUSER_USERNAME" ]; then
    python manage.py createsuperuser --noinput 2>/dev/null || true
fi

# Populate CV data if the database is empty (idempotent — skips if data exists).
python manage.py populate_cv

echo "Starting gunicorn..."
exec gunicorn config.wsgi:application --bind 0.0.0.0:8000 --workers 2
