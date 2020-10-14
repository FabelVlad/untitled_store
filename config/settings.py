# -*- coding: utf-8 -*-

from __future__ import absolute_import, unicode_literals

import os
import sys

import sentry_sdk
from environ import environ
from sentry_sdk.integrations.django import DjangoIntegration

ROOT_DIR = environ.Path(__file__) - 2
APPS_DIR = ROOT_DIR.path('store_apps')

env = environ.Env(
    DJANGO_DEBUG=(bool, True),
    DJANGO_SECRET_KEY=(str, ''),
    DJANGO_ADMINS=(list, []),
    DJANGO_ALLOWED_HOSTS=(list, ['*']),
    DJANGO_STATIC_ROOT=(str, str(APPS_DIR('staticfiles'))),
    DJANGO_MEDIA_ROOT=(str, str(APPS_DIR('media'))),
    DJANGO_DATABASE_URL=(str, f'sqlite:////{str(ROOT_DIR)}\\django_sqlite.db'),
    DJANGO_EMAIL_URL=(environ.Env.email_url_config, 'consolemail://'),
    DJANGO_DEFAULT_FROM_EMAIL=(str, 'admin@example.com'),
    DJANGO_SERVER_EMAIL=(str, 'root@localhost.com'),
    DJANGO_STRIPE_PUBLIC_KEY=(str, ''),
    DJANGO_STRIPE_SECRET_KEY=(str, ''),
    DJANGO_TEST_RUN=(bool, False),
    DJANGO_HEALTH_CHECK_BODY=(str, 'Success'),
)

environ.Env.read_env(env_file=os.path.join(str(ROOT_DIR), '.env'))

DEBUG = env.bool("DJANGO_DEBUG", default=False)

SECRET_KEY = env('DJANGO_SECRET_KEY')

ALLOWED_HOSTS = env.list('DJANGO_ALLOWED_HOSTS')

ADMINS = tuple([tuple(admins.split(':')) for admins in env.list('DJANGO_ADMINS')])

MANAGERS = ADMINS

TIME_ZONE = 'UTC'

LANGUAGE_CODE = 'en-us'

SITE_ID = 2

USE_I18N = True

USE_L10N = True

USE_TZ = True

DATABASES = {
    'default': env.db('DJANGO_DATABASE_URL')
}

if DEBUG is False:
    import dj_database_url

    DATABASES['default'].update(dj_database_url.config(conn_max_age=600, ssl_require=True))

DJANGO_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.admin',
    'django.contrib.humanize',
)

THIRD_PARTY_APPS = (
    'imagekit',
    'ckeditor',
    'django_filters',
    'stripe'
)

LOCAL_APPS = (
    'store_apps.users.apps.UsersConfig',
    'store_apps.products.apps.ProductsConfig',
    'store_apps.payments.apps.PaymentsConfig',
)

INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + LOCAL_APPS

AUTH_USER_MODEL = 'users.User'
ADMIN_URL = r'^admin/'
LOGIN_URL = 'users:login'
LOGIN_REDIRECT_URL = 'home'
LOGOUT_REDIRECT_URL = 'home'

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',

]

""" Settings for mailling """

EMAIL_BACKEND = env('DJANGO_EMAIL_BACKEND')
EMAIL_FILE_PATH = env('', default=f'{ROOT_DIR}/app_mails')
EMAIL_HOST = env('DJANGO_EMAIL_HOST')
EMAIL_HOST_PASSWORD = env('DJANGO_EMAIL_HOST_PASSWORD')
EMAIL_HOST_USER = env('DJANGO_EMAIL_HOST_USER')
EMAIL_PORT = env.int('DJANGO_EMAIL_PORT')
EMAIL_USE_TLS = env.bool('DJANGO_EMAIL_USE_TLS')
EMAIL_USE_SSL = env.bool('DJANGO_EMAIL_USE_SSL', default=False)
EMAIL_SSL_CERTFILE = env('DJANGO_EMAIL_SSL_CERTFILE', default=None)
EMAIL_SSL_KEYFILE = env('DJANGO_EMAIL_SSL_KEYFILE', default=None)
# EMAIL_TIMEOUT

DEFAULT_FROM_EMAIL = env('DJANGO_DEFAULT_FROM_EMAIL')
SERVER_EMAIL = env('DJANGO_SERVER_EMAIL')

TEMPLATES = [
    {
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
            ],
        },
    },
]

STATIC_URL = '/static/'
STATIC_ROOT = env('DJANGO_STATIC_ROOT')

MEDIA_URL = '/media/'
MEDIA_ROOT = env('DJANGO_MEDIA_ROOT')

STATICFILES_DIRS = (
    str(APPS_DIR.path('static')),
)

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
)

ROOT_URLCONF = 'config.urls'

WSGI_APPLICATION = 'config.wsgi.application'

AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
)

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
            'level': 'WARN',
        },
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True
        },
        'django.db.backends': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True
        },
        'store_apps.payments.stripe_service': {
            'handlers': ['mail_admins'],
            'propagate': True,
            'level': 'WARN',
        },
    }
}

""" Settings for Sentry https://docs.sentry.io/platforms/python/guides/django/ """

USE_SENTRY = env.bool('DJANGO_USE_SENTRY')
if USE_SENTRY:
    sentry_sdk.init(
        dsn=env.str('DJANGO_SENTRY_DSN'),
        integrations=[DjangoIntegration()],
        send_default_pii=True
    )

if DEBUG:
    MIDDLEWARE += [
        'debug_toolbar.middleware.DebugToolbarMiddleware',
    ]
    INSTALLED_APPS += (
        'debug_toolbar',
    )
    DEBUG_TOOLBAR_CONFIG = {
        'DISABLE_PANELS': [
            'debug_toolbar.panels.redirects.RedirectsPanel',
        ],
        'SHOW_TEMPLATE_CONTEXT': True,
        'SHOW_TOOLBAR_CALLBACK': lambda request: True,
    }

    DEBUG_TOOLBAR_PATCH_SETTINGS = False

    # http://django-debug-toolbar.readthedocs.org/en/latest/installation.html
    INTERNAL_IPS = ('127.0.0.1', '0.0.0.0', '10.0.2.2',)

if env.bool('DJANGO_TEST_RUN'):
    pass

HEALTH_CHECK_BODY = env('DJANGO_HEALTH_CHECK_BODY')

STRIPE_PUBLIC_KEY = env.str('DJANGO_STRIPE_PUBLIC_KEY')
STRIPE_SECRET_KEY = env.str('DJANGO_STRIPE_SECRET_KEY')

""" Settings for django-filter """

FILTERS_EMPTY_CHOICE_LABEL = 'All'

""" Sessions settings """

SESSION_ENGINE = 'django.contrib.sessions.backends.cached_db'

""" Cache settings """

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
        'LOCATION': '127.0.0.1:11211',
    }
}
