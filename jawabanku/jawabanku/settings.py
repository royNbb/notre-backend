"""
Django settings for jawabanku project.

Generated by 'django-admin startproject' using Django 3.1.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.1/ref/settings/
"""

import os
from datetime import timedelta
from pathlib import Path

from colorlog import ColoredFormatter
from dotenv import load_dotenv

load_dotenv()

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent
env_path = BASE_DIR / '.env'


def envbool(s: str, default: str) -> bool:
  v = os.getenv(s, default=default)
  if v not in ("", "True", "False"):
    msg = "Unexpected value %s=%s, use 'True' or 'False'" % (s, v)
    raise Exception(msg)

  return v == "True"


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.1/howto/deployment/checklist/
ENVIRONMENT = os.getenv("ENVIRONMENT", "development")
DEVELOPMENT_ENVIRONMENT = ENVIRONMENT == "development"

DEBUG = envbool("DEBUG", "False")

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv("SECRET_KEY")
# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['api.notescentre.com']

# Application definition

INSTALLED_APPS = [
    "django.contrib.admin.apps.SimpleAdminConfig",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "corsheaders",
    "rest_framework",
    "djoser",
    "django_admin_logs",
    "account",
    "material",
    "comment",
    "report",
    "history",
    "common",
]

MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "djangorestframework_camel_case.middleware.CamelCaseMiddleWare",
]

CORS_ALLOW_CREDENTIALS = True
CORS_ALLOWED_ORIGINS = [
    'http://localhost:8000',
    'http://localhost:3000',
    'https://api.notescentre.com',
    'https://www.notescentre.com',
    'https://notescentre.com',
]
CSRF_TRUSTED_ORIGINS = [
    'http://localhost:8000',
    'http://localhost:3000',
    'https://api.notescentre.com',
    'https://www.notescentre.com',
    'https://notescentre.com',
]

ROOT_URLCONF = "jawabanku.urls"

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

WSGI_APPLICATION = "jawabanku.wsgi.application"


AUTHENTICATION_BACKENDS = [
    "django.contrib.auth.backends.ModelBackend",
]


DJOSER = {
    'SERIALIZERS': {
        'current_user': 'account.serializers.AccountSerializer',
    }
}

# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql_psycopg2",
        "NAME": os.getenv("DB_NAME"),
        "USER": os.getenv("DB_USER"),
        "PASSWORD": os.getenv("DB_PASS"),
        "HOST": os.getenv("DB_HOST"),
        "PORT": 5432,
    },
}

AUTH_USER_MODEL = "account.Account"

# Password validation
# https://docs.djangoproject.com/en/3.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


# Internationalization
# https://docs.djangoproject.com/en/3.1/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.1/howto/static-files/

STATIC_ROOT = BASE_DIR / '../staticfiles'
STATIC_URL = '/static/'

LOGGING_DIR = os.path.join(BASE_DIR, "logs")
os.makedirs(LOGGING_DIR, exist_ok=True)

LOGGING_LEVEL = "DEBUG"  # Adjust this based on your needs

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "verbose": {
            "()": ColoredFormatter,
            "format": "[{log_color}{levelname}{reset}][{asctime}][{module}]|{message}",
            "style": "{",
            "log_colors": {
                "DEBUG": "white",
                "INFO": "green",
                "WARNING": "yellow",
                "ERROR": "bold_red",
                "CRITICAL": "bold_red",
            },
        },
        "simple": {
            "format": "[{levelname}]|{message}",
            "style": "{",
        },
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "level": "DEBUG" if DEBUG else "INFO",
            "formatter": "verbose",
        },
        "rotate_file": {
            "level": LOGGING_LEVEL,
            "class": "logging.handlers.RotatingFileHandler",
            "filename": os.path.join(LOGGING_DIR, "app.log"),
            "maxBytes": 1024 * 1024 * 20,  # 20 MB
            "backupCount": 5,  # Number of backup files to keep
            "formatter": "verbose",
        },
    },
    "root": {
        "handlers": ["rotate_file"],
        "level": LOGGING_LEVEL,
    },
}

REST_FRAMEWORK = {
    "DATETIME_FORMAT": "%s000",  # converts 10 digits unix to 13 digits (Js convention)
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "rest_framework_simplejwt.authentication.JWTAuthentication",
    ),
    "DEFAULT_THROTTLE_CLASSES": [
        "rest_framework.throttling.AnonRateThrottle",
        "rest_framework.throttling.UserRateThrottle",
    ],
    "DEFAULT_THROTTLE_RATES": {
        "anon": "5/second",
        "user": "10/second",
    },
    "DEFAULT_RENDERER_CLASSES": (
        "djangorestframework_camel_case.render.CamelCaseJSONRenderer",
        "djangorestframework_camel_case.render.CamelCaseBrowsableAPIRenderer",
    ),
    "DEFAULT_PARSER_CLASSES": (
        "djangorestframework_camel_case.parser.CamelCaseFormParser",
        "djangorestframework_camel_case.parser.CamelCaseMultiPartParser",
        "djangorestframework_camel_case.parser.CamelCaseJSONParser",
    ),
}

SIMPLE_JWT = {
    "AUTH_HEADER_TYPES": ("JWT",),
    "ACCESS_TOKEN_LIFETIME": timedelta(days=15),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=30),
    "SIGNING_KEY": SECRET_KEY,
}


if DEVELOPMENT_ENVIRONMENT:
  LOGGING["root"]["handlers"].append("console")



### for gcs credential
from google.oauth2 import service_account
GS_CREDENTIALS = service_account.Credentials.from_service_account_file(
  os.path.join(BASE_DIR.parent,"credential.json")
)

GOOGLE_APPLICATION_CREDENTIALS = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
print(GOOGLE_APPLICATION_CREDENTIALS)
 ###configuration for media file storing and reriving media file from gcloud 
DEFAULT_FILE_STORAGE='django_blog_project.gcloud.GoogleCloudMediaFileStorage'
GS_PROJECT_ID = 'notre-v-1 '
GS_BUCKET_NAME = os.getenv("GCS_BUCKET_NAME")
MEDIA_ROOT = "media/"
UPLOAD_ROOT = 'media/uploads/'
MEDIA_URL = 'https://storage.googleapis.com/{}/'.format(GS_BUCKET_NAME)
