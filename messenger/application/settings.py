from os import path
from pathlib import Path

try:
    from .local_settings import *
except ImportError:
    pass

BASE_DIR = Path(__file__).resolve().parent.parent

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django_celery_results',
    'django_celery_beat',
    'oauth2_provider',
    'drf_social_oauth2',
    'rest_framework',
    'social_django',
    'users',
    'chats',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'application.middleware.LoginRequiredMiddleware'
]

AUTHENTICATION_BACKENDS = [
    'social_core.backends.google.GoogleOAuth2',
    'django.contrib.auth.backends.ModelBackend'
]

LOGIN_URL = '/login/'
LOGIN_REDIRECT_URL = 'http://localhost:3000/'
LOGOUT_URL = '/logout/'
LOGOUT_REDIRECT_URL = 'http://localhost:3000/'

SOCIAL_AUTH_GOOGLE_OAUTH2_KEY = GOOGLE_CLIENT_ID
SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = GOOGLE_CLIENT_SECRET

ROOT_URLCONF = 'application.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            path.join(BASE_DIR, 'templates'),
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'social_django.context_processors.backends',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'application.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': DB_NAME,
        'USER': DB_USER,
        'PASSWORD': DB_PASSWORD,
        'HOST': '127.0.0.1',
        'PORT': 5432
    }
}

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

MEDIA_URL = '/media/'
MEDIA_ROOT = path.join(BASE_DIR, 'media/')

STATIC_URL = '/static/'

STATICFILES_DIRS = [
    path.join(BASE_DIR, 'static')
]

LOGIN_IGNORE_URLS = [
    '/login/',
    '/logout/',
    '/admin/',
    '/auth/',
    '/social-auth/'
]

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


AUTH_USER_MODEL = 'users.User'

CORS_ORIGIN_WHITELIST = [
    'http://localhost:8000/',
    'http://127.0.0.1:8000/',
    'http://127.0.0.1:3000/',
    'http://localhost:3000/',
]

CELERY_IMPORTS = ('chats.tasks',)

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.yandex.ru'
EMAIL_PORT = 465
EMAIL_USE_TLS = False
EMAIL_USE_SSL = True
