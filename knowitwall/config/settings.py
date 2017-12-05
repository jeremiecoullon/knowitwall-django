import os
import sys
# if working locally
if os.path.isfile('le_local_setup.txt'):
    import config.local_settings

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
import sys
sys.path.append('{}/knowitwall'.format(BASE_DIR))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.10/howto/deployment/checklist/


if os.path.isfile('le_local_setup.txt'):
    SECRET_KEY = config.local_settings.SECRET_KEY
else:
    SECRET_KEY = os.environ['SECRET_KEY']

if os.path.isfile('le_local_setup.txt'):
    DEBUG = True
else:
    DEBUG = False

ALLOWED_HOSTS = ["kiw-august-test.us-west-2.elasticbeanstalk.com", "localhost"]


# Application definition
AWS_PRELOAD_METADATA = True

INSTALLED_APPS = [
    'storages',
    'ckeditor_uploader',
    'ckeditor',
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


if 'RDS_DB_NAME' in os.environ:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql_psycopg2',
            'NAME': os.environ['RDS_DB_NAME'],
            'USER': os.environ['RDS_USERNAME'],
            'PASSWORD': os.environ['RDS_PASSWORD'],
            'HOST': os.environ['RDS_HOSTNAME'],
            'PORT': os.environ['RDS_PORT'],
        }
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql_psycopg2',
            'NAME': config.local_settings.DATABASE_NAME,
            'USER': config.local_settings.LOCAL_PSQL_USERNAME,
            'PASSWORD': config.local_settings.LOCAL_PSQL_PASSWORD,
            'HOST': '',
            'PORT': '',
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
        'toolbar': 'Full',
        # 'extraPlugins': 'wordcount',
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
        'toolbar': 'Full',
        'height': 700,
        'width': 1100,
        "allowedContent": True
    },
}
# STATICFILES_DIRS = [
#     os.path.join(BASE_DIR, "static"),
#     # '/var/www/static/',
# ]
# STATIC_ROOT = 'static/'

# AWS_URL = "https://s3.eu-west-2.amazonaws.com/knowitwall"

#MEDIA FILE (user uploaded files)
MEDIA_ROOT = os.path.join(BASE_DIR, "..", "www", "media")
MEDIA_URL = '/media/'
STATIC_ROOT = os.path.join(BASE_DIR, "..", "www", "static")
STATIC_URL = '/static/'

# AWS storage stuff
# AWS_STORAGE_BUCKET_NAME = 'knowitwall-test-2'

# if working locally
# if os.path.isfile('le_local_setup.txt'):
#     AWS_ACCESS_KEY_ID = config.local_settings.LE_AWS_ACCESS_KEY_ID
#     AWS_SECRET_ACCESS_KEY = config.local_settings.LE_AWS_SECRET_ACCESS_KEY
# else: # else if on elasticbeanstalk
#     AWS_ACCESS_KEY_ID = os.environ['LE_AWS_ACCESS_KEY_ID']
#     AWS_SECRET_ACCESS_KEY = os.environ['LE_AWS_SECRET_ACCESS_KEY']
#
# # if deployed
# if 'RDS_DB_NAME' in os.environ:
#     AWS_S3_CUSTOM_DOMAIN = '%s.s3.amazonaws.com' % AWS_STORAGE_BUCKET_NAME
#     STATIC_URL = "https://%s/" % AWS_S3_CUSTOM_DOMAIN
#     STATICFILES_LOCATION = 'knowitwall/static'
#     MEDIAFILES_LOCATION = 'knowitwall/media'
#     import custom_storages
#     STATICFILES_STORAGE = 'custom_storages.StaticStorage'
#     DEFAULT_FILE_STORAGE = 'custom_storages.MediaStorage'
#     STATIC_URL = "https://%s/%s/" % (AWS_S3_CUSTOM_DOMAIN, STATICFILES_LOCATION)
#     MEDIA_URL = "https://%s/%s/" % (AWS_S3_CUSTOM_DOMAIN, MEDIAFILES_LOCATION)



# email stuff
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
ADMIN_LIST = ['jeremie.coullon@gmail.com']
# if working locally, get email info
if os.path.isfile('le_local_setup.txt'):
    EMAIL_HOST_USER = config.local_settings.EMAIL_HOST_USER
    EMAIL_HOST_PASSWORD = config.local_settings.EMAIL_HOST_PASSWORD
else:
    EMAIL_HOST_USER = os.environ['EMAIL_HOST_USER']
    EMAIL_HOST_PASSWORD = os.environ['EMAIL_HOST_PASSWORD']
