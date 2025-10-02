#!/bin/bash

# Simple build script for Render deployment
echo "Starting build process..."

# Upgrade pip
pip install --upgrade pip

# Install requirements
pip install -r requirements.txt

# Collect static files
python manage.py collectstatic --noinput

echo "Build completed successfully!"
