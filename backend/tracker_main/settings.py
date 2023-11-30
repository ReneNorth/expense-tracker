import logging
import os
from pathlib import Path

from django.utils.log import DEFAULT_LOGGING
from dotenv import load_dotenv

log = logging.getLogger(__name__)
BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR.parent / 'infra/.env')


# https://docs.djangoproject.com/en/4.2/topics/settings/
SECRET_KEY = os.getenv("DJANGO_KEY")
HOST = os.getenv("HOST", default="http://127.0.0.1:8000/")

DEBUG = True

ALLOWED_HOSTS = []


INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    'rest_framework',
    "expenses.apps.ExpensesConfig",
    "users.apps.UsersConfig",
    "tgbot.apps.TgbotConfig",
    "api.apps.ApiConfig",

]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

# REST_FRAMEWORK = {
#     'DEFAULT_PERMISSION_CLASSES': [
#         'rest_framework.permissions.IsAuthenticatedOrReadOnly',
#     ],

#     'DEFAULT_AUTHENTICATION_CLASSES': [
#         'rest_framework_simplejwt.authentication.JWTAuthentication',
#         'rest_framework.authentication.SessionAuthentication'
#     ],

#     'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
#     'PAGE_SIZE': 6,
# }


ROOT_URLCONF = "tracker_main.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR.parent / 'frontend' / 'templates'],
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

WSGI_APPLICATION = "tracker_main.wsgi.application"


# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}


# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

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


LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True


STATIC_URL = 'frontend/static/'
STATICFILES_DIRS = [
    BASE_DIR.parent / 'frontend/static'
]
STATIC_ROOT = BASE_DIR.parent / 'frontend' / 'local-cdn' / 'static'

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"


LOGLEVEL = 'DEBUG'
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {process:d} {thread:d} {message}',
            'style': '{',
        },
        'simple': {
            'format': '{levelname} {message}',
            'style': '{',
        },
        'django.server': DEFAULT_LOGGING['formatters']['django.server'],
    },
    'handlers': {
        'console': {
            'level': f'{LOGLEVEL}',
            'class': 'logging.StreamHandler',
            'formatter': 'simple',
        },
        'django.server': DEFAULT_LOGGING['handlers']['django.server'],
    },
    'loggers': {
        '': {
            'level': LOGLEVEL,
            'handlers': ['console', ],
        },
        'django.server': DEFAULT_LOGGING['loggers']['django.server'],
        'django.template': {
            'handlers': ['console'],
            'level': os.getenv('DJANGO_LOG_LEVEL', 'DEBUG'),
        },
    }
}
