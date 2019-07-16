import os
from urllib.parse import urlparse
from .base import *

# Database
# https://docs.djangoproject.com/en/2.2/ref/settings/#databases
DB_URL = os.environ['DB_URL']
PARSED_DB_URL = urlparse(DB_URL)
DB_NAME = PARSED_DB_URL.path[1:]
DB_USER = PARSED_DB_URL.username
DB_HOST = PARSED_DB_URL.hostname
DB_PWD = PARSED_DB_URL.password
DB_PORT = PARSED_DB_URL.port

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': DB_NAME,
        'USER': DB_USER,
        'PASSWORD': DB_PWD,
        'HOST': DB_HOST,
        'PORT': DB_PORT,
    }
}