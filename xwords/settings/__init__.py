import os
from .secret import *
from celery.schedules import crontab

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

DEBUG = True
NO_CACHE = False
DETERMINISTIC_RATE = 0.2 # KEEP THIS BETWEEN 0 and 1!

ALLOWED_HOSTS = [
    "127.0.0.1",
    "0.0.0.0",
    "localhost",
    "xwords.sites.tjhsst.edu"
]

INSTALLED_APPS = [
    'django.contrib.auth',
    'django.contrib.admin',
    'django.contrib.messages',
    'django.contrib.postgres',
    'django.contrib.sessions',
    'django.contrib.staticfiles',
    'django.contrib.contenttypes',
    'channels',
    'django_celery_results',
    'xwords.apps',
    'xwords.apps.api.apps.ApiConfig',
    'xwords.apps.crosswords.apps.CrosswordsConfig',
]

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

ROOT_URLCONF = 'xwords.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, "templates")],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]


ASGI_APPLICATION = 'xwords.routing.application'
WSGI_APPLICATION = 'xwords.wsgi.application'
SESSION_ENGINE = "django.contrib.sessions.backends.signed_cookies"


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': DB_NAME,
        'USER': DB_USER,
        'PASSWORD': DB_PASSWORD,
        'HOST': DB_HOST,
        'PORT': DB_PORT
    }
}

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'EST'
USE_I18N = True
USE_L10N = True
USE_TZ = True

STATIC_URL = '/static/'
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
STATIC_ROOT = os.path.join(BASE_DIR, "static")


CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels_redis.core.RedisChannelLayer',
        'CONFIG': {
            "hosts": [(REDIS_HOST, REDIS_PORT)],
        },
    },
}

# Celery
CELERY_RESULT_BACKED = "django-db" 
CELERY_BROKER_URL = "redis://{}:{}/1".format(REDIS_HOST, REDIS_PORT)
CELERY_TIMEZONE = "America/New_York"
CELERY_BEAT_SCHEDULE = {
    'delete-crossword-copies':{
        'task': 'xwords.apps.crosswords.tasks.delete_crossword_copies',
        'schedule': crontab(hour=2,minute=30,day_of_week='*/2'),
        'args': (),
    }
}

# Crossword Settings
CROSSWORD_ROOT = os.path.join(BASE_DIR, "crosswords")

LANGUAGE_CHOICES = [
    ("en", "English"),
    ("de", "German"),
    ("fr", "French"),
    ("es", "Spanish"),
    ("hu", "Hungarian")
]

