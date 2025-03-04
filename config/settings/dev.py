from .base import *

DATABASES = {
'default': {
'ENGINE': 'django.db.backends.postgresql',
'NAME': 'minpj',
'USER': 'parkim',
'PASSWORD': '1234',
'HOST': 'localhost',
'PORT': '5432',
}
}

ROOT_URLCONF = 'config.urls.urls_dev'