"""
Django settings for insurance project.

Generated by 'django-admin startproject' using Django 3.1.3.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.1/ref/settings/
"""
from datetime import timedelta
from pathlib import Path

import environ

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Read .env
environ.Env.read_env()
env = environ.Env()

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env.str(
    "SECRET_KEY", default="*06-8gkx=yc^zp&ihkcuy4am0*+dt&ariuv68y1sj0%vya^$@@"
)

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = env.bool("DEBUG", False)

ALLOWED_HOSTS = env.list("ALLOWED_HOSTS", default=["*"])

CORS_ALLOW_ALL_ORIGINS = env.bool("CORS_ALLOW_ALL_ORIGINS", True)


# Application definition

INSTALLED_APPS = [
    "jet.dashboard",
    "jet",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "corsheaders",
    "rest_framework",
    "rest_framework_gis",
    "rest_framework.authtoken",
    "djoser",
    "drf_spectacular",
    "dry_rest_permissions",
    "django_filters",
    "django.contrib.gis",
    "drf_extra_fields",
    "api.apps.ApiConfig",
    "sensors.apps.SensorsConfig",
    "contracts.apps.ContractsConfig",
    "dbbackup",
    "django_cron",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "corsheaders.middleware.CorsPostCsrfMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "django.middleware.locale.LocaleMiddleware",
]

ROOT_URLCONF = "insurance.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "insurance.wsgi.application"


# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases

DATABASES = {
    "default": {
        **env.db(
            "DATABASE_URL",
            default="postgresql://insurance:secret@insurance-db:5432/insurance",
        ),
        "ENGINE": "django.contrib.gis.db.backends.postgis",
    }
}


# Password validation
# https://docs.djangoproject.com/en/3.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",},
]


# Internationalization
# https://docs.djangoproject.com/en/3.1/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "Europe/Kiev"

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.1/howto/static-files/

STATIC_URL = "/static-backend/"
STATIC_ROOT = "static"

# Media files

MEDIA_URL = "/media/"
MEDIA_ROOT = "media"

# User model

AUTH_USER_MODEL = "api.User"

# Django REST Framework

REST_FRAMEWORK = {
    "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.PageNumberPagination",
    "PAGE_SIZE": env.int("PAGE_SIZE", 50),
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "rest_framework_simplejwt.authentication.JWTAuthentication",
    ),
    "DEFAULT_RENDERER_CLASSES": (
        "rest_framework.renderers.JSONRenderer",
        "rest_framework.renderers.BrowsableAPIRenderer",
    ),
    "DEFAULT_SCHEMA_CLASS": "drf_spectacular.openapi.AutoSchema",
    "DEFAULT_METADATA_CLASS": "rest_framework.metadata.SimpleMetadata",
    "DEFAULT_FILTER_BACKENDS": ("django_filters.rest_framework.DjangoFilterBackend",),
}

# Simple JWT

ACCESS_TOKEN_LIFETIME_MINUTES = env.int("ACCESS_TOKEN_LIFETIME_MINUTES", default=6 * 60)
REFRESH_TOKEN_LIFETIME_DAYS = env.int("REFRESH_TOKEN_LIFETIME_DAYS", default=1)
REFRESH_TOKEN_LIFETIME_MINUTES = env.int("REFRESH_TOKEN_LIFETIME_DAYS", default=30)

SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(minutes=ACCESS_TOKEN_LIFETIME_MINUTES),
    "REFRESH_TOKEN_LIFETIME": timedelta(
        days=REFRESH_TOKEN_LIFETIME_DAYS, minutes=REFRESH_TOKEN_LIFETIME_MINUTES
    ),
}

# Djoser

DJOSER = {
    "SERIALIZERS": {
        "user_create": "api.serializers.MyUserCreateSerializer",
        "current_user": "api.serializers.CurrentUserSerializer",
    },
}

# AWS
AWS_ACCESS_KEY_ID = env.str("AWS_ACCESS_KEY_ID", None)
AWS_SECRET_ACCESS_KEY = env.str("AWS_SECRET_ACCESS_KEY", None)
AWS_S3_REGION_NAME = env.str("AWS_S3_REGION_NAME", default="eu-central-1")

AWS_S3_SIGNATURE_VERSION = env.str("AWS_S3_SIGNATURE_VERSION", default="s3v4")
AWS_QUERYSTRING_AUTH = env.bool("AWS_QUERYSTRING_AUTH", default=True)
AWS_DEFAULT_ACL = env.str("AWS_DEFAULT_ACL", None)  # "public-read" for public buckets

USE_AWS_FOR_MEDIA = env.bool("USE_AWS_FOR_MEDIA", False)
USE_AWS_FOR_STATIC = env.bool("USE_AWS_FOR_STATIC", False)

if USE_AWS_FOR_MEDIA:
    DEFAULT_FILE_STORAGE = "api.storages.S3MediaStorage"

if USE_AWS_FOR_STATIC:
    STATICFILES_STORAGE = "api.storages.S3StaticStorage"

AWS_S3_STATIC_BUCKET_NAME = env.str(
    "AWS_S3_STATIC_BUCKET_NAME", default="smart-auto-insurance"
)
AWS_S3_MEDIA_BUCKET_NAME = env.str(
    "AWS_S3_MEDIA_BUCKET_NAME", default="smart-auto-insurance"
)

# JET

X_FRAME_OPTIONS = "SAMEORIGIN"

# MyMappi

MYMAPPI_API_KEY = env.str("MYMAPPI_API_KEY", default=None)


# Intervals for sensors

SPEED_RECORD_MAX_INTERVAL = env.int("SPEED_RECORD_MAX_INTERVAL", default=10)
HEAD_ANGLE_RECORD_MAX_INTERVAL = env.int("HEAD_ANGLE_RECORD_MAX_INTERVAL", default=3)


# BACKUPS

DBBACKUP_STORAGE = "django.core.files.storage.FileSystemStorage"
DBBACKUP_STORAGE_OPTIONS = {"location": "/usr/src/app/backup/"}

DBBACKUP_CONNECTOR_MAPPING = {
    "django.contrib.gis.db.backends.postgis": "dbbackup.db.postgresql.PgDumpGisConnector",
}

CRON_CLASSES = [
    "cron.backup.BackupJob",
]
