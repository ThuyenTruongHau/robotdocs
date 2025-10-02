"""
Fallback settings for deployment without database
"""

from .settings import *

# Override database to use SQLite for fallback
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# Disable database-dependent features
INSTALLED_APPS = [
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'corsheaders',
    'drf_yasg',
    'apps.core',
    'apps.users',
    'apps.product',
    'apps.category',
    'apps.brand',
]

# Disable auth for fallback
AUTH_USER_MODEL = None
