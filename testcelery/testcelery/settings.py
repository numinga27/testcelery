"""
Django settings for testcelery project.

Generated by 'django-admin startproject' using Django 3.1.10.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.1/ref/settings/
"""

from pathlib import Path
import logging
import os


# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent
# LOG_DIR = os.path.join(BASE_DIR, 'logs')
# # Создаем директорию, если она не существует
# if not os.path.exists(LOG_DIR):
#     os.makedirs(LOG_DIR)

# # Настройки логирования
# LOGGING = {
#     'version': 1,
#     'disable_existing_loggers': False,
#     'formatters': {  # Форматирование сообщений
#         'verbose': {
#             'format': '{levelname} {asctime} {module} {message}',
#             'style': '{',
#         },
#     },
#     'handlers': {  # Обработчики
#         'file': {
#             'class': 'logging.FileHandler',
#             'filename': os.path.join(LOG_DIR, 'celer.log'),  # Путь к файлу логов Celery
#             'formatter': 'verbose',
#         },
#     },
#     'loggers': {
#         'celery': {  # Настройки логгера для Celery
#             'handlers': ['file'],
#             'level': 'INFO',
#             'propagate': False,
#         },
#     },
# }


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'ai^1a6r=jkh!fer%v$g2@)ug6ii&8px0zkh_145%%ys%hiqqca'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'testing',
    'celery',
    'channels',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    # 'channels.middleware.ChannelsMiddleware',
]

ROOT_URLCONF = 'testcelery.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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

WSGI_APPLICATION = 'testcelery.wsgi.application'
ASGI_APPLICATION = "testcelery.routing.application"

CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels_redis.core.RedisChannelLayer",
        "CONFIG": {
            "hosts": [('127.0.0.1', 6379)],
        },
    },
}
# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': BASE_DIR / 'db.sqlite3',
#     }
# }
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'db_4',
        'USER': 'postgres',
        'PASSWORD': 'user',
        'HOST': 'localhost',
        'PORT': '5432',
        # 'ATOMIC_REQUESTS': True,  # Включение повторной попытки запросов
        # 'CONN_MAX_AGE': 0.001,  # Время ожидания блокировки в секундах
    }
}

# Password validation
# https://docs.djangoproject.com/en/3.1/ref/settings/#auth-password-validators

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


# Internationalization
# https://docs.djangoproject.com/en/3.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.1/howto/static-files/

STATIC_URL = '/static/'
CELERY_BROKER_URL = 'redis://localhost:6379/0'
# CELERY_BROKER_URL = 'redis://localhost:6379/0'
CELERY_RESULT_BACKEND = 'redis://localhost:6379/0'
CELERY_ACCEPT_CONTENT = ['application/json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TIMEZONE = 'Europe/Moscow'
CELERY_BEAT_SCHEDULE = {
    'parse-every-30-seconds': {
        'task': 'testing.tasks.send_request_task',
        'schedule': 10.0,
    },
}
CACHE_MIDDLEWARE_SECONDS = 0