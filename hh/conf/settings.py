"""
Django settings for conf project.

Generated by 'django-admin startproject' using Django 4.0.

For more information on this file, see
https://docs.djangoproject.com/en/4.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.0/ref/settings/
"""
import os
from pathlib import Path

from . import local_settings

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = local_settings.SECRET_KEY

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = local_settings.DEBUG

ALLOWED_HOSTS = local_settings.ALLOWED_HOSTS

# Application definition

INSTALLED_APPS = [
    # builtin
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.humanize',

    # installed
    'crispy_forms',
    'cities_light',
    'smart_selects',
    'el_pagination',
    'notifications',
    'floppyforms',

    # custom
    'conf',
    'accounts.apps.AccountsConfig',
    'blog.apps.BlogConfig',
    'resumes.apps.ResumesConfig',
    'vacancies.apps.VacanciesConfig',
    'recruiting.apps.RecruitingConfig',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'conf.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'django.template.context_processors.request',  # For EL-pagination
                'blog.context_processor.recent_news',
            ],
        },
    },
]

WSGI_APPLICATION = 'conf.wsgi.application'

# Database
# https://docs.djangoproject.com/en/4.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# Password validation
# https://docs.djangoproject.com/en/4.0/ref/settings/#auth-password-validators

if DEBUG:
    AUTH_PASSWORD_VALIDATORS = []
else:
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


AUTH_USER_MODEL = 'accounts.Account'


# Internationalization
# https://docs.djangoproject.com/en/4.0/topics/i18n/

TIME_ZONE = 'Europe/Moscow'

USE_I18N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.0/howto/static-files/
STATIC_URL = "/static/"
STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'templates'),
)

# Media files
MEDIA_URL = 'media/'
MEDIA_ROOT = BASE_DIR.joinpath('media')

LOCALE_PATHS = (os.path.join(BASE_DIR, 'locale'),)

# Default primary key field type
# https://docs.djangoproject.com/en/4.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

try:
    os.makedirs(BASE_DIR.joinpath('logs'))  # make "logs" directory if not exists
except FileExistsError:
    pass

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'default': {
            'format': '{levelname}, {asctime}, {module}, {process:d}/{thread:d} - {message}',
            'style': '{',
        },
    },
    'handlers': {
        'django_server': {
            'level': 'WARNING',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': f'{BASE_DIR.joinpath("logs").joinpath("django_server.log")}',
            'maxBytes': 1024 * 1024 * 5,
            'backupCount': 5,
            'formatter': 'default',
        },
        'accounts_file': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': f'{BASE_DIR.joinpath("logs").joinpath("accounts.log")}',
            'formatter': 'default',
        },
        'resumes_file': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': f'{BASE_DIR.joinpath("logs").joinpath("resumes.log")}',
            'formatter': 'default',
        },
        'vacancies_file': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': f'{BASE_DIR.joinpath("logs").joinpath("vacancies.log")}',
            'formatter': 'default',
        },
        'blog_file': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': f'{BASE_DIR.joinpath("logs").joinpath("blog.log")}',
            'formatter': 'default',
        },
    },
    'loggers': {
        'django.server': {
            'handlers': ['django_server'],
            'propagate': True,
        },
        'accounts': {
            'handlers': ['accounts_file'],
            'level': 'DEBUG',
            'propagate': True,
        },
        'resumes': {
            'handlers': ['resumes_file'],
            'level': 'DEBUG',
            'propagate': True,
        },
        'vacancies': {
            'handlers': ['vacancies_file'],
            'level': 'DEBUG',
            'propagate': True,
        },
        'blog': {
            'handlers': ['blog_file'],
            'level': 'DEBUG',
            'propagate': True,
        },
    },
}


LOGIN_REDIRECT_URL = '/'
LOGIN_URL = '/'
LOGOUT_REDIRECT_URL = '/'

CRISPY_TEMPLATE_PACK = 'bootstrap4'

USE_I18N = True
USE_L10N = False

LANGUAGE_CODE = 'ru-ru'
LANGUAGES = (
    ('ru', 'русский'),
    ('en', 'english'),
)

DATE_FORMAT = 'd E Y'

CITIES_LIGHT_TRANSLATION_LANGUAGES = ['ru']
CITIES_LIGHT_INCLUDE_COUNTRIES = ['RU']
CITIES_LIGHT_INCLUDE_CITY_TYPES = ['PPL', 'PPLA', 'PPLA2', 'PPLA3', 'PPLA4', 'PPLC', 'PPLF', 'PPLG', 'PPLL', 'PPLR', 'PPLS', 'STLMT',]
