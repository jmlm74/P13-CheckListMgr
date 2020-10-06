import os

from .settings import *
# just for Travis !!!
SECRET_KEY = get_env_variable('SECRET_KEY', "nxx(or0igwys!l7q60i2c_3a36v59k2qtx3ze%4wn#-!18hn#b")
# postgres database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'testdb',
        'USER': 'postgres',
        'PASSWORD': '',
        'HOST': '',
        'PORT': '',
    },
}
