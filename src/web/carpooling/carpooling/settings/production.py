"""
Production settings for carpooling project.
"""
from .base import *

DEBUG = False

TEMPLATE_DEBUG = False

INSTALLED_APPS += (
)

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

WSGI_APPLICATION = 'carpooling.wsgi.production.application'
