import os
import sys
from .utils import get_env_variable

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


SECRET_KEY = get_env_variable("SECRET_KEY")

if os.path.isfile("../../prod.txt"):
    DEBUG = False
else:
    DEBUG = True


ALLOWED_HOSTS = ["165.227.237.83", "localhost", "knowitwall.com", "www.knowitwall.com"]


INSTALLED_APPS = [
    'ckeditor_uploader',
    'ckeditor',
    'team.apps.TeamConfig',
    'content.apps.ContentConfig',
    'notifications.apps.NotificationsConfig',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
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

ROOT_URLCONF = 'config.urls'

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

WSGI_APPLICATION = 'config.wsgi.application'


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        # 'NAME': get_env_variable('RDS_DB_NAME'),
        # read different database while chaging db schema for "Seasons"
        'NAME': 'kiw_seasons_db',
        'USER': get_env_variable('RDS_USERNAME'),
        'PASSWORD': get_env_variable('RDS_PASSWORD'),
        'HOST': "",
        'PORT': "",
        # 'HOST': get_env_variable('RDS_HOSTNAME'),
        # 'PORT': get_env_variable('RDS_PORT'),
    }
}

# Password validation
# https://docs.djangoproject.com/en/1.10/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/1.10/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.10/howto/static-files/
CKEDITOR_UPLOAD_PATH = "uploads/"
CKEDITOR_CONFIGS = {
    'default': {
        'toolbar': 'Custom',
        'toolbar_Custom': [
            ['Link', 'Unlink', 'Blockquote', 'Image', 'Italic', 'Bold', 'Underline', 'SpecialChar', 'Source'],
        ],
        "autoParagraph": False,
    },
    'image_credits': {
        'toolbar': 'Custom',
        'toolbar_Custom': [
            ['Italic'],
            ['Link', 'Unlink'],
        ],
        'height': 100,
        'width': 1000,
    },
    'small': {
        'toolbar': 'Custom',
        'toolbar_Custom': [
            []
        ],
        'height': 100,
        'width': 1000,
    },
    'transcript': {
        'toolbar': 'Custom',
        'toolbar_Custom': [
            ['Link', 'Unlink', 'Blockquote', 'Image', 'Italic', 'Bold', 'Underline', 'SpecialChar', 'Source'],
        ],
        'height': 700,
        'width': 1100,
        "allowedContent": True
    },
}

#MEDIA FILE (user uploaded files)
MEDIA_ROOT = os.path.join(BASE_DIR, "..", "www", "media")
MEDIA_URL = '/media/'
STATIC_ROOT = os.path.join(BASE_DIR, "..", "www", "static")
STATIC_URL = '/static/'

FILE_UPLOAD_MAX_MEMORY_SIZE = 200000000

# email stuff
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
ADMIN_LIST = ['jeremie.coullon@gmail.com']
EMAIL_HOST_USER = get_env_variable('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = get_env_variable('EMAIL_HOST_PASSWORD')
