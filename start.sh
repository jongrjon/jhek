#!/bin/bash
set -e

echo "Running migrations..."
python manage.py migrate --noinput

# Create superuser from env vars if set and user doesn't exist yet.
if [ -n "$DJANGO_SUPERUSER_USERNAME" ]; then
    python manage.py createsuperuser --noinput 2>/dev/null || true
fi

echo "Starting gunicorn..."
exec gunicorn config.wsgi:application --bind 0.0.0.0:8000 --workers 2
