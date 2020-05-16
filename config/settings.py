# -*- coding: utf-8 -*-
import sys
import logging

import environ


# frontend_internship_templates_training/config/settings.py - 2 = frontend_internship_templates_training/
ROOT_DIR = environ.Path(__file__) - 2
APPS_DIR = ROOT_DIR.path('frontend_internship_templates_training')
sys.path.append('frontend_internship_templates_training/apps')

# Environment
# https://django-environ.readthedocs.io/en/latest/#how-to-use
# ------------------------------------------------------------------------------
# Default values and casting
env = environ.Env(
    DJANGO_DEBUG=(bool, False),
    DJANGO_SECRET_KEY=(str, ''),
    DJANGO_ADMINS=(list, []),
    DJANGO_ALLOWED_HOSTS=(list, []),
    # Static/Media
    DJANGO_STATIC_ROOT=(str, str(APPS_DIR('staticfiles'))),
    DJANGO_MEDIA_ROOT=(str, str(APPS_DIR('media'))),
    # Database
    POSTGRES_HOST=(str, 'db'),
    POSTGRES_PORT=(int, 5432),
    POSTGRES_DB=(str, ''),
    POSTGRES_USER=(str, ''),
    POSTGRES_PASSWORD=(str, ''),
    # Email
    DJANGO_EMAIL_URL=(environ.Env.email_url_config, 'consolemail://'),
    DJANGO_EMAIL_BACKEND=(str, 'django.core.mail.backends.smtp.EmailBackend'),
    DJANGO_DEFAULT_FROM_EMAIL=(str, 'admin@example.com'),
    DJANGO_SERVER_EMAIL=(str, 'root@localhost.com'),
    # Debug
    DJANGO_TEST_RUN=(bool, False),
)

# Django Core
# https://docs.djangoproject.com/en/2.2/ref/settings/#core-settings
# ------------------------------------------------------------------------------
DEBUG = env.bool("DJANGO_DEBUG")
SECRET_KEY = env('DJANGO_SECRET_KEY')
ROOT_URLCONF = 'config.urls'
WSGI_APPLICATION = 'config.wsgi.application'
ALLOWED_HOSTS = env.list('DJANGO_ALLOWED_HOSTS')
ADMINS = tuple([
    tuple(admins.split(':'))
    for admins in env.list('DJANGO_ADMINS')
])
MANAGERS = ADMINS
ADMIN_URL = 'admin/'
ADMIN_SITE_TITLE = 'Frontend Internship Templates Traning'
ADMIN_SITE_HEADER = 'Frontend Internship Templates Traning'
TIME_ZONE = 'UTC'
USE_TZ = True
LANGUAGE_CODE = 'en-us'
USE_I18N = True
USE_L10N = True
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
DATA_UPLOAD_MAX_MEMORY_SIZE = 20_971_520  # 20MB
FILE_UPLOAD_MAX_MEMORY_SIZE = 20_971_520  # 20MB

# Django Sites
# https://docs.djangoproject.com/en/2.2/ref/settings/#sites
# ------------------------------------------------------------------------------
SITE_ID = 1

# Django Database
# https://docs.djangoproject.com/en/2.2/ref/settings/#databases
# ------------------------------------------------------------------------------
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': env('POSTGRES_DB'),
        'USER': env('POSTGRES_USER'),
        'PASSWORD': env('POSTGRES_PASSWORD'),
        'HOST': env('POSTGRES_HOST'),
        'PORT': env('POSTGRES_PORT'),
    }
}

# Django Applications
# https://docs.djangoproject.com/en/2.2/ref/settings/#installed-apps
# ------------------------------------------------------------------------------
DJANGO_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.admin',
)
THIRD_PARTY_APPS = (
    'django_extensions',
    'ckeditor',
    'widget_tweaks',
    'easy_thumbnails',
)
LOCAL_APPS = (
    'flatpages.apps.FlatpagesConfig',
)
INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + LOCAL_APPS

# Django Middlewares
# https://docs.djangoproject.com/en/2.2/ref/settings/#middleware
# ------------------------------------------------------------------------------
MIDDLEWARE = [
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# Django Email Server
# https://docs.djangoproject.com/en/2.2/ref/settings/#email-backend
# ------------------------------------------------------------------------------
EMAIL_URL = env.email_url('DJANGO_EMAIL_URL')
EMAIL_BACKEND = EMAIL_URL['EMAIL_BACKEND']
EMAIL_HOST = EMAIL_URL.get('EMAIL_HOST', '')
EMAIL_HOST_PASSWORD = EMAIL_URL.get('EMAIL_HOST_PASSWORD', '')
EMAIL_HOST_USER = EMAIL_URL.get('EMAIL_HOST_USER', '')
EMAIL_PORT = EMAIL_URL.get('EMAIL_PORT', '')
EMAIL_USE_SSL = 'EMAIL_USE_SSL' in EMAIL_URL
EMAIL_USE_TLS = 'EMAIL_USE_TLS' in EMAIL_URL
EMAIL_FILE_PATH = EMAIL_URL.get('EMAIL_FILE_PATH', '')
EMAIL_SUBJECT_PREFIX = ''
DEFAULT_FROM_EMAIL = env('DJANGO_DEFAULT_FROM_EMAIL')
SERVER_EMAIL = env('DJANGO_SERVER_EMAIL')

# Django Templates
# https://docs.djangoproject.com/en/2.2/ref/settings/#templates
# ------------------------------------------------------------------------------
TEMPLATES = [{
    'BACKEND': 'django.template.backends.django.DjangoTemplates',
    'DIRS': [
        str(APPS_DIR.path('templates')),
    ],
    'OPTIONS': {
        'debug': DEBUG,
        'loaders': [
            'django.template.loaders.filesystem.Loader',
            'django.template.loaders.app_directories.Loader',
        ],
        'context_processors': [
            'django.template.context_processors.debug',
            'django.template.context_processors.request',
            'django.contrib.auth.context_processors.auth',
            'django.template.context_processors.i18n',
            'django.template.context_processors.media',
            'django.template.context_processors.static',
            'django.template.context_processors.tz',
            'django.contrib.messages.context_processors.messages',
            'flatpages.context_processors.flatpages',
        ],
    },
}]

# Django Logging
# https://docs.djangoproject.com/en/2.2/ref/settings/#logging
# ------------------------------------------------------------------------------
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        },
        'require_debug_true': {
            '()': 'django.utils.log.RequireDebugTrue',
        },
    },
    'formatters': {
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(module)s '
                      '%(process)d %(thread)d %(message)s'
        },
    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        },
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'verbose',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'propagate': True,
            'level': 'INFO',
        },
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'INFO',
            'propagate': True
        },
    }
}

# Django Static Files
# https://docs.djangoproject.com/en/2.2/ref/settings/#static-files
# ------------------------------------------------------------------------------
STATIC_URL = '/static/'
STATIC_ROOT = env('DJANGO_STATIC_ROOT')
STATICFILES_DIRS = (
    str(APPS_DIR.path('static')),
)
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
)

# Django Media Files
# https://docs.djangoproject.com/en/2.2/ref/settings/#media-root
# ------------------------------------------------------------------------------
MEDIA_URL = '/media/'
MEDIA_ROOT = env('DJANGO_MEDIA_ROOT')

# Django Auth
# https://docs.djangoproject.com/en/2.2/ref/settings/#auth
# ------------------------------------------------------------------------------
AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
)
LOGIN_REDIRECT_URL = '/'
