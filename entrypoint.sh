#!/bin/sh
# Run any pending migrations without prompting
python manage.py migrate --no-input

# Replace this shell with Gunicorn serving your app
exec gunicorn f1_dashboard.wsgi:application --bind 0.0.0.0:8000