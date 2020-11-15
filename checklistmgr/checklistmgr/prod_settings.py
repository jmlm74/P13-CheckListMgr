

from .settings import *

# debug
DEBUG = False
TEMPLATE_DEBUG = False
PRODUCTION = True

# disable django debug toolbar
INTERNAL_IPS = []

# security
ALLOWED_HOSTS = ['*', ]
SECRET_KEY = get_env_variable('SECRET_KEY', '')
if not DEBUG:
    try:
        INSTALLED_APPS.remove('django.contrib.admin')
    except ValueError:
        pass

# postgres database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': get_env_variable('DATABASE_NAME', ''),
        'USER': get_env_variable('DATABASE_USER', ''),
        'PASSWORD': get_env_variable('DATABASE_PSW', ''),
        'HOST': get_env_variable('DATABASE_HOST', ''),
        'PORT': '5432',
    }
}
WSGI_APPLICATION = 'checklistmgr.wsgi.application'

# static files
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

# logging
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'file': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'filename': '/var/log/django/django.log',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['file'],
            'level': 'INFO',
            'propagate': True,
        },
    },
}

