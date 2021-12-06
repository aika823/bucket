import os
from pathlib import Path
import json

# DEBUG
DEBUG = True

# Base
BASE_DIR = Path(__file__).resolve().parent.parent
ROOT_DIR = os.path.dirname(BASE_DIR)
# PROJECT_ROOT    = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PROJECT_ROOT = os.path.abspath(os.path.dirname(__name__))
MEDIA_ROOT = os.path.join(BASE_DIR, "media")


# URL
PROJECT_URL = "http://localhost:8000"
# PROJECT_URL = 'http://billim.co.kr'
# PROJECT_URL = 'http://bucket-env.eba-mfepamsq.ap-northeast-2.elasticbeanstalk.com'
IMAGE_URL = "http://static.billim.co.kr"
# SERVICE_URL = json.load(open('url.json'))['SERVICE_URL']
# IMAGE_URL = json.load(open('url.json'))['IMAGE_URL']
MEDIA_URL = "/media/"

# SECRET
SECRET_DIR = os.path.join(PROJECT_ROOT, "secret")
SECRETS = json.load(open(os.path.join(SECRET_DIR, "secret.json"), "rb"))
DB_SECRETS = json.load(open(os.path.join(SECRET_DIR, "database.json"), "rb"))
SECRET_KEY = SECRETS["SECRET_KEY"]

# HOSTS
ALLOWED_HOSTS = [
    "localhost",
    "127.0.0.1",
    "bucketlister.co.kr",
    "bucket-env.eba-mfepamsq.ap-northeast-2.elasticbeanstalk.com",
]

# Application definition
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.shortcuts",
    "six",
    "api",
    "user",
    "party",
    "rest_framework",
    "storages",
    "manager",
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

ROOT_URLCONF = "bucket.urls"

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

WSGI_APPLICATION = "bucket.wsgi.application"

# Database
DATABASES = {
    "default": {
        "ENGINE": DB_SECRETS["ENGINE"],
        "NAME": DB_SECRETS["NAME"],
        "USER": DB_SECRETS["USER"],
        "PASSWORD": DB_SECRETS["PASSWORD"],
        "HOST": DB_SECRETS["HOST"],
        "PORT": DB_SECRETS["PORT"],
        "OPTIONS": DB_SECRETS["OPTIONS"],
    }
}

# Password validation
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
LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_L10N = True
USE_TZ = True

# STATIC SETTINGS
STATIC_URL = "/static/"
# STATIC_ROOT = os.path.join(BASE_DIR, "static")
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "static"),
    os.path.join(BASE_DIR, "static/css"),
    os.path.join(BASE_DIR, "static/images"),
    os.path.join(BASE_DIR, "static/js"),
    "static/css",
    "static/js",
    "static/images",
]

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# AWS API SETTINGS
AWS_ACCESS_KEY_ID = SECRETS["AWS_ACCESS_KEY_ID"]
AWS_SECRET_ACCESS_KEY = SECRETS["AWS_SECRET_ACCESS_KEY"]
AWS_REGION = "ap-northeast-2"

# AWS S3 SETTINGS
# AWS_STORAGE_BUCKET_NAME = "static.buckitlister.co.kr"
# AWS_S3_CUSTOM_DOMAIN = "%s.s3.%s.amazonaws.com" % (AWS_STORAGE_BUCKET_NAME, AWS_REGION)
# AWS_S3_OBJECT_PARAMETERS = {
#     "CacheControl": "max-age=86400",
# }
# DEFAULT_FILE_STORAGE = "storages.backends.s3boto3.S3Boto3Storage"

# SOCIAL API SETTINGS
NAVER_CLIENT_ID = SECRETS["NAVER_CLIENT_ID"]
NAVER_CLIENT_SECRET = SECRETS["NAVER_CLIENT_SECRET"]
NAVER_CLOUD_CLIENT_ID = SECRETS["NAVER_CLOUD_CLIENT_ID"]
NAVER_CLOUD_CLIENT_SECRET = SECRETS["NAVER_CLOUD_CLIENT_SECRET"]
KAKAO_CLIENT_ID = SECRETS["KAKAO_CLIENT_ID"]
GOOGLE_CLIENT_ID = SECRETS["GOOGLE_CLIENT_ID"]
GOOGLE_CLIENT_SECRET = SECRETS["GOOGLE_CLIENT_SECRET"]

# EMAIL API SETTINGS
EMAIL_HOST = "smtp.gmail.com"
EMAIL_PORT = "587"
EMAIL_HOST_USER = "choiinkyu95@gmail.com"
EMAIL_HOST_PASSWORD = "frjerzmtqcsniqeb"
EMAIL_USE_TLS = True
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER