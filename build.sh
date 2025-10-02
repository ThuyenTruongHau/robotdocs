#!/bin/bash

# Build script for Render deployment
echo "Starting build process..."

# Upgrade pip and install build tools
pip install --upgrade pip setuptools wheel

# Install requirements with verbose output
echo "Installing Python dependencies..."
pip install -r requirements.txt --verbose

# Verify Django installation
echo "Verifying Django installation..."
python -c "import django; print(f'Django version: {django.get_version()}')"

# Verify Gunicorn installation
echo "Verifying Gunicorn installation..."
python -c "import gunicorn; print('Gunicorn installed successfully')"

# Verify psycopg installation
echo "Verifying psycopg installation..."
python -c "import psycopg; print('psycopg installed successfully')" || echo "WARNING: psycopg not found"

# Collect static files
echo "Collecting static files..."
python manage.py collectstatic --noinput

echo "Build completed successfully!"
