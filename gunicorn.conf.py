# Gunicorn configuration file for Render deployment

import multiprocessing
import os

# Server socket
bind = "0.0.0.0:8000"

# Worker processes
workers = 2  # Reduced for Render free tier
worker_class = "sync"
timeout = 30
keepalive = 2

# Logging
accesslog = "-"
errorlog = "-"
loglevel = "info"

# Environment variables
raw_env = [
    'DJANGO_SETTINGS_MODULE=core.settings',
]

# Preload app for better performance
preload_app = True
