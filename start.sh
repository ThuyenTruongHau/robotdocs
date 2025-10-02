#!/bin/bash

# Production startup script for Thado Robot Backend

# Set environment variables
export DJANGO_SETTINGS_MODULE=core.settings

# Check if Django is installed
echo "Checking Django installation..."
python -c "import django; print(f'Django {django.get_version()} is available')" || {
    echo "ERROR: Django is not installed!"
    exit 1
}

# Check if Gunicorn is installed
echo "Checking Gunicorn installation..."
python -c "import gunicorn; print('Gunicorn is available')" || {
    echo "ERROR: Gunicorn is not installed!"
    exit 1
}

# Check database connection
echo "Checking database connection..."
python -c "
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
import django
django.setup()
from django.db import connection
try:
    connection.ensure_connection()
    print('Database connection successful')
except Exception as e:
    print(f'Database connection failed: {e}')
    print('Starting without database...')
" || {
    echo "WARNING: Database connection failed, starting without database..."
}

# Run database migrations (only if database is available)
echo "Running database migrations..."
python manage.py migrate || {
    echo "WARNING: Database migration failed, continuing without database..."
}

# Start Gunicorn server
echo "Starting Gunicorn server..."
exec gunicorn --config gunicorn.conf.py core.wsgi:application
