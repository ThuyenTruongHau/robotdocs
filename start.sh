#!/bin/bash

# Production startup script for Thado Robot Backend

# Set environment variables
export DJANGO_SETTINGS_MODULE=core.settings

# Run database migrations
echo "Running database migrations..."
python manage.py migrate

# Start Gunicorn server
echo "Starting Gunicorn server..."
exec gunicorn --config gunicorn.conf.py core.wsgi:application
