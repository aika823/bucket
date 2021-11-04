import os
from pathlib import Path
import json

# DEBUG
DEBUG = True

# Base
BASE_DIR = Path(__file__).resolve().parent.parent
ROOT_DIR = os.path.dirname(BASE_DIR)
PROJECT_ROOT    = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# URL
BILLIM_URL = 'http://localhost:8000'
# BILLIM_URL = 'http://billim.co.kr'
IMAGE_URL = 'http://static.billim.co.kr'

# SECRET
SECRET_DIR = os.path.join(PROJECT_ROOT, 'secret')
SECRETS = json.load(open(os.path.join(SECRET_DIR, 'secret.json'), 'rb'))
DB_SECRETS = json.load(open(os.path.join(SECRET_DIR, 'database.json'), 'rb'))
SECRET_KEY = SECRETS['SECRET_KEY']
# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-@wv*@c%ur&-_9shg%b3jfnki5gvd^)j+&g+qo2o0o5j*)v(k(6'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = [
    '127.0.0.1',
    'bucket-env.eba-mfepamsq.ap-northeast-2.elasticbeanstalk.com'
]


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'api',
    'user',
    'rest_framework',
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

ROOT_URLCONF = 'bucket.urls'

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

WSGI_APPLICATION = 'bucket.wsgi.application'


# Database
DATABASES = {
    'default': {
        'ENGINE': DB_SECRETS['ENGINE'],
        'NAME': DB_SECRETS['NAME'],
        'USER': DB_SECRETS['USER'],
        'PASSWORD': DB_SECRETS['PASSWORD'],
        'HOST': DB_SECRETS['HOST'],
        'PORT': DB_SECRETS['PORT'],
        'OPTIONS': DB_SECRETS['OPTIONS']
    }
}



# Password validation
# https://docs.djangoproject.com/en/3.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/3.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/

STATIC_URL = '/static/'

# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# API SETTINGS
AWS_ACCESS_KEY_ID           = SECRETS['AWS_ACCESS_KEY_ID']
AWS_SECRET_ACCESS_KEY       = SECRETS['AWS_SECRET_ACCESS_KEY']
AWS_REGION                  = 'ap-northeast-2'
AWS_STORAGE_BUCKET_NAME     = 'static.billim.co.kr'
AWS_S3_CUSTOM_DOMAIN        = '%s.s3.%s.amazonaws.com' % (AWS_STORAGE_BUCKET_NAME,AWS_REGION)
AWS_S3_OBJECT_PARAMETERS    = {'CacheControl': 'max-age=86400',}
DEFAULT_FILE_STORAGE        = 'storages.backends.s3boto3.S3Boto3Storage'

NAVER_CLIENT_ID             = SECRETS['NAVER_CLIENT_ID']
NAVER_CLOUD_CLIENT_ID       = SECRETS['NAVER_CLOUD_CLIENT_ID']
NAVER_CLOUD_CLIENT_SECRET   = SECRETS['NAVER_CLOUD_CLIENT_SECRET']

KAKAO_CLIENT_ID             = SECRETS['KAKAO_CLIENT_ID']
