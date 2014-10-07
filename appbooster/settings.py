"""
Django settings for appbooster project.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.7/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
from os import path
BASE_DIR = os.path.dirname(os.path.dirname(__file__))
PROJECT_DIR = BASE_DIR

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.7/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '&ixcc*e%v$9%z6cc+ebavawkf586jpo8w2yy-#!g&2znddohip'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'appbooster.urls'

WSGI_APPLICATION = 'appbooster.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.7/ref/settings/#databases

if os.environ.get('ENVIRONMENT', 'dev') == 'dev':
    DATABASE_ENGINE = 'django.db.backends.sqlite3',
else:
    DATABASE_ENGINE = 'django.db.backends.mysql'

DATABASES = {
    'default': {
        'ENGINE': DATABASE_ENGINE,
        'NAME': 'appdb',
        'USER': 'appbooster',
        'PASSWORD': 'appbooster',
        'HOST': '',
        'PORT': '',
    },
}

# Internationalization
# https://docs.djangoproject.com/en/1.7/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'US/Eastern'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.7/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = ''
STATICFILES_DIRS = (
    path.join(PROJECT_DIR, 'static'),
)

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
#    'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

TEMPLATE_DIRS = (
    path.abspath(path.join(PROJECT_DIR, "templates")),
)

TEMPLATE_CONTEXT_PROCESSORS = (
   # ...
   'django.core.context_processors.request',
   'django.contrib.auth.context_processors.auth',
   # ...
)

EMAIL_USE_TLS = True
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = 'purdueseats@gmail.com'
EMAIL_HOST_PASSWORD = 'purduecourse!'
EMAIL_PORT = 587

FIXTURE_DIRS = (
    path.join(PROJECT_DIR, 'fixtures'),
)

LOGIN_URL = '/login/'
LOGIN_REDIRECT_URL = '/dashboard/'