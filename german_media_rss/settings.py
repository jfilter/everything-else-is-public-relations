"""
Django settings for german_media_rss project.

Generated by 'django-admin startproject' using Django 2.0.

For more information on this file, see
https://docs.djangoproject.com/en/2.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.0/ref/settings/
"""

import os
import re
from typing import Dict, Union  # noqa

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv("SECRET_KEY", "override me")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True if os.getenv("NODEBUG") is None else False

# TODO: Change your domain names here.
ALLOWED_HOSTS = ["web", "localhost"] if os.getenv("NODEBUG") is None else [".rss-suche.vis.one"]

# Application definition

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sites",
    "django.contrib.sessions",
    "django.contrib.messages",
    "whitenoise.runserver_nostatic",
    "django.contrib.staticfiles",
    "django_extensions",
    "raven.contrib.django.raven_compat",
    "huey.contrib.djhuey",
    "main",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "german_media_rss.stats_middleware.StatsMiddleware",
    "raven.contrib.django.raven_compat.middleware.SentryResponseErrorIdMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.contrib.sites.middleware.CurrentSiteMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "german_media_rss.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [os.path.join(BASE_DIR, "templates")],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ]
        },
    }
]

WSGI_APPLICATION = "german_media_rss.wsgi.application"

AUTH_USER_MODEL = "main.User"

# Adjust this to taste.
SESSION_ENGINE = "django.contrib.sessions.backends.cached_db"

if os.getenv("IN_DOCKER"):
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.postgresql_psycopg2",
            "NAME": "postgres",
            "USER": "postgres",
            "PASSWORD": "password",
            "HOST": "db",
            "PORT": 5432,
        }
    }

    CACHES = {
        "default": {
            "BACKEND": "django_redis.cache.RedisCache",
            "LOCATION": "redis://redis/1",
            "OPTIONS": {"CLIENT_CLASS": "django_redis.client.DefaultClient"},
        }
    }

    SESSION_CACHE_ALIAS = "default"
    SESSION_COOKIE_AGE = 365 * 24 * 60 * 60
elif os.getenv("DATABASE_URL"):
    # Running under Dokku.
    USER, PASSWORD, HOST, PORT, NAME = re.match(  # type: ignore
        "^postgres://(?P<username>.*?)\:(?P<password>.*?)\@(?P<host>.*?)\:(?P<port>\d+)\/(?P<db>.*?)$",
        os.getenv("DATABASE_URL", ""),
    ).groups()

    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.postgresql_psycopg2",
            "NAME": NAME,
            "USER": USER,
            "PASSWORD": PASSWORD,
            "HOST": HOST,
            "PORT": int(PORT),
        }
    }

    CACHES = {
        "default": {
            "BACKEND": "django_redis.cache.RedisCache",
            "LOCATION": os.getenv("REDIS_URL", "") + "/1",
            "OPTIONS": {"CLIENT_CLASS": "django_redis.client.DefaultClient"},
        }
    }

    SESSION_CACHE_ALIAS = "default"
    SESSION_ENGINE = "django.contrib.sessions.backends.cache"
    SESSION_COOKIE_AGE = 365 * 24 * 60 * 60
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
else:
    DATABASES = {"default": {"ENGINE": "django.db.backends.sqlite3", "NAME": os.path.join(BASE_DIR, "db.sqlite3")}}

if os.getenv("EMAIL_HOST_PASSWORD", ""):
    # TODO: Change these to match your provider.
    EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"

    EMAIL_USE_TLS = True
    EMAIL_HOST = "smtp.sendgrid.net"
    EMAIL_HOST_USER = "apikey"
    EMAIL_HOST_PASSWORD = os.getenv("EMAIL_HOST_PASSWORD", "")
    EMAIL_PORT = 587
else:
    EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"


# Password validation
# https://docs.djangoproject.com/en/2.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

# Internationalization
# https://docs.djangoproject.com/en/2.0/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_L10N = True

USE_TZ = True

SITE_ID = 1

RAVEN_CONFIG = {"dsn": os.getenv("RAVEN_DSN")}  # type: Dict[str, Union[None, str]]

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {"console": {"class": "logging.StreamHandler"}},
    "loggers": {"django": {"handlers": ["console"], "level": os.getenv("DJANGO_LOG_LEVEL", "INFO")}},
}

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.0/howto/static-files/

STATIC_URL = "/static/"
STATIC_ROOT = os.path.join(BASE_DIR, "_static")
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"
STATICFILES_DIRS = [os.path.join(BASE_DIR, "static")]

try:
    from .local_settings import *  # noqa
    from .local_settings import LOCAL_INSTALLED_APPS, LOCAL_MIDDLEWARE  # type: ignore
except ImportError:
    pass

try:
    INSTALLED_APPS += LOCAL_INSTALLED_APPS
except:  # noqa
    pass

try:
    MIDDLEWARE += LOCAL_MIDDLEWARE
except:  # noqa
    pass

if os.getenv("IN_DOCKER"):
    HUEY = {
        'name': 'huey_db',  # Use db name for huey.
        'consumer': {
            'workers': 20,
            'worker_type': 'thread',
        },
        'connection': {
            'host': 'redis',
            'port': 6379,
            'db': 1,
        },
        'always_eager': False
    }
else:
    HUEY = {
        'name': 'huey_db',  # Use db name for huey.
        'consumer': {
            'workers': 20,
            'worker_type': 'thread',
        },
        'connection': {
            'url': os.getenv("REDIS_URL")
        },
    }
