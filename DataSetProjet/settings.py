# settings.py

from pathlib import Path
import os

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = 'django-insecure-e@$=-8r%@0y!oe=rpeyqrffi3=g7^zi2n&2v%t_xnjxbqn0+0#'

DEBUG = True

ALLOWED_HOSTS = []

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'DataSetsApp',
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

ROOT_URLCONF = 'DataSetProjet.urls'

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
            ],
        },
    },
]

WSGI_APPLICATION = 'DataSetProjet.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    },
    'my_database': {
        'ENGINE': 'djongo',
        'NAME': 'my_database',
        'ENFORCE_SCHEMA': False,
        'CLIENT': {
            'host': 'mongodb',
            'port': 27017,
            'username': 'root',
            'password': 'pass12345',
            'authSource': 'admin',
            'authMechanism': 'SCRAM-SHA-1',
        },
    },
    'my_database_images': {
        'ENGINE': 'djongo',
        'NAME': 'my_database_images',
        'ENFORCE_SCHEMA': False,
        'CLIENT': {
            'host': 'mongodb',
            'port': 27017,
            'username': 'root',
            'password': 'pass12345',
            'authSource': 'admin',
            'authMechanism': 'SCRAM-SHA-1',
        },
    }
}

DATABASE_ROUTERS = ['DataSetProjet.database_router.DatabaseRouter']

LOGIN_REDIRECT_URL = 'list_datasets'
LOGOUT_REDIRECT_URL = 'login'

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

LANGUAGE_CODE = 'fr-FR'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True

DATA_UPLOAD_MAX_MEMORY_SIZE = 26214400  # 25 MB
FILE_UPLOAD_MAX_MEMORY_SIZE = 26214400  # 25 MB
DATA_UPLOAD_MAX_NUMBER_FILES = 100  # qu'on peut ajuster

STATIC_URL = 'static/'
APPEND_SLASH = True

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Configuration de la connexion MongoDB
MONGO_URI = 'mongodb://root:pass12345@localhost:27017/'
MONGO_DB_NAME = 'my_database'
