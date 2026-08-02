import json
import os
from decimal import Decimal
from pathlib import Path

from decouple import Csv, config

BASE_DIR = Path(__file__).resolve().parent.parent
SECRET_KEY = config("SECRET_KEY")
DEBUG = config("DEBUG", default=False, cast=bool)

ALLOWED_HOSTS = config("ALLOWED_HOSTS", cast=Csv(), default="*")

CSRF_TRUSTED_ORIGINS = [
    "http://localhost",
    "http://127.0.0.1",
    # "http://10.17.18.7" # local production server IP ,
]

INTERNAL_IPS = ["127.0.0.1"]



INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    "django_htmx",
    "widget_tweaks",
    "crispy_forms",
    "crispy_bootstrap5",
    "django.contrib.humanize",

    "apps.administration",
    "apps.graduates",
]


if DEBUG:
    INSTALLED_APPS.append("debug_toolbar")
    INSTALLED_APPS.append("django_extensions")


MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]
if DEBUG:
    MIDDLEWARE.append("debug_toolbar.middleware.DebugToolbarMiddleware")


ROOT_URLCONF = 'core.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
         "DIRS": [BASE_DIR / "templates"],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                "django.template.context_processors.media",
                "core.context_processors.global_context",
            ],
        },
    },
]

WSGI_APPLICATION = 'core.wsgi.application'


# Database
_use_postgres = bool(config("DB_NAME", default=""))

DATABASES = {
    "default": (
        {
            "ENGINE": "django.db.backends.postgresql_psycopg2",
            "NAME": config("DB_NAME"),
            "USER": config("DB_USER"),
            "PASSWORD": config("DB_PASSWORD"),
            "HOST": config("DB_HOST", default="localhost"),
            "PORT": config("DB_PORT", default="5432"),
        }
        if _use_postgres
        else {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": BASE_DIR / "db.sqlite3",
        }
    ),
}



# Password validation
# https://docs.djangoproject.com/en/6.0/ref/settings/#auth-password-validators

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


AUTHENTICATION_BACKENDS = [
    "apps.administration.backends.UsersProfileAuthBackend",
    "django.contrib.auth.backends.ModelBackend",  # للوصول إلى Django Admin
]

LANGUAGE_CODE = "ar-EG"

TIME_ZONE = "Africa/Cairo"

USE_I18N = True

USE_L10N = True

USE_TZ = True


STATIC_URL = "static/"
STATICFILES_DIRS = [BASE_DIR / "static"]
STATIC_ROOT = BASE_DIR / "staticfiles"

MEDIA_URL = "/uploads/"
MEDIA_ROOT = os.path.join(BASE_DIR, "uploads")

BACKUP_ROOT = BASE_DIR / "backups"

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

CRISPY_ALLOWED_TEMPLATE_PACKS = "bootstrap5"
CRISPY_TEMPLATE_PACK = "bootstrap5"

LOGIN_URL = "administration:login"
LOGOUT_REDIRECT_URL = "administration:login"

SESSION_COOKIE_AGE = 1800  # 30 minutes of inactivity
SESSION_EXPIRE_AT_BROWSER_CLOSE = True
SESSION_SAVE_EVERY_REQUEST = True


DATA_UPLOAD_MAX_NUMBER_FIELDS = 10000
DATA_UPLOAD_MAX_MEMORY_SIZE = 10 * 1024 * 1024  # 10 MB

APPLICATION_NAME = "نظام بداية لإدارة مركز الشهادات"
APPLICATION_SLUG = "شهادتي"
HOME_PAGE_TITLE = "الرئيسية"
LOGIN_PAGE_TITLE = "تسجيل الدخول"
ORDER_PAGE_TITLE = "الطلبات"
COPYRIGHT_NAME = "شركة بداية لتسويق خدمات جامعة بنها (شركة مملوكة بالكامل لجامعة بنها)"
COPYRIGHT_YEAR = "2026"

LOGS_DIR = BASE_DIR / "logs"
LOGS_DIR.mkdir(exist_ok=True)

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "verbose": {
            "format": "{asctime} | {levelname} | {module} | {message}",
            "style": "{",
            "datefmt": "%Y-%m-%d %H:%M:%S",
        },
        "simple": {
            "format": "{asctime} | {levelname} | {message}",
            "style": "{",
            "datefmt": "%Y-%m-%d %H:%M:%S",
        },
    },
    "handlers": {
        "console": {
            "level": "INFO",
            "class": "logging.StreamHandler",
            "formatter": "simple",
        },
        "file": {
            "level": "WARNING",
            "class": "logging.handlers.RotatingFileHandler",
            "filename": LOGS_DIR / "certificates_center.log",
            "maxBytes": 10485760,
            "backupCount": 10,
            "formatter": "verbose",
            "delay": True,
            "encoding": "utf-8",
        },
    },
    "root": {
        "handlers": ["console", "file"],
        "level": "INFO" if DEBUG else "WARNING",
    },
    "loggers": {
        "django": {
            "handlers": ["console", "file"],
            "level": "INFO" if DEBUG else "ERROR",
            "propagate": False,
        },
        "django.security": {
            "handlers": ["console", "file"] if not DEBUG else ["console"],
            "level": "WARNING",
            "propagate": False,
        },
        "inventory_control": {
            "handlers": ["console", "file"],
            "level": "DEBUG" if DEBUG else "INFO",
            "propagate": False,
        },
    },
}


class DjangoJSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Decimal):
            return float(obj)
        return super().default(obj)


JSON_ENCODER = "core.settings.DjangoJSONEncoder"
