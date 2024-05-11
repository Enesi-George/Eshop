"""
Django settings for Eshop project.

Generated by 'django-admin startproject' using Django 5.0.4.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.0/ref/settings/
"""

import os
from pathlib import Path
from dotenv import load_dotenv
from datetime import timedelta
from django.utils.functional import LazyObject, empty
import cloudinary

load_dotenv()


class MyTokenObtainPairViewLazy(LazyObject):
    def _setup(self):
        from account.views import MyTokenObtainPairView

        self._wrapped = MyTokenObtainPairView()


MyTokenObtainPairView = MyTokenObtainPairViewLazy


# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

DEFAULT_APP_URL = os.getenv("DEFAULT_APP_URL")

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv("SECRET_KEY")
TEMPLATES_DIR = os.path.join(BASE_DIR, "templates")


# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.getenv("DJANGO_DEBUG")

ALLOWED_HOSTS = []

# Register User model in admin
REGISTER_USER_MODEL = True


# Application definition

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    # authentication
    "account",
    "shop",
    "rest_framework.authtoken",
    "rest_framework_simplejwt",
    "djoser",
    "rest_framework",
    "cloudinary",
    "cloudinary_storage",
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

REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "rest_framework_simplejwt.authentication.JWTAuthentication",
    ),
}
MY_APP_NAME = os.getenv("MY_APP_NAME")

SIMPLE_JWT = {
    "AUTH_HEADER_TYPES": ("JWT", "Bearer"),
    "ACCESS_TOKEN_LIFETIME": timedelta(days=5),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=5),
    "ROTATE_REFRESH_TOKENS": False,
    "BLACKLIST_AFTER_ROTATION": False,
    # use the custom token serializer
    "TOKEN_SERIALIZER": MyTokenObtainPairView,
    # add the custom claims to the token
    "CLAIMS": {
        "name": "auth.name",
        "role": "auth.role",
        "email": "auth.email",
        "is_staff": "auth.is_staff",
        "username": "auth.username",
    },
}

# authentication
DJOSER = {
    "SEND_ACTIVATION_EMAIL": True,
    "SEND_CONFIRMATION_EMAIL": True,
    "PASSWORD_CHANGED_EMAIL_CONFIRMATION": True,
    "USERNAME_CHANGED_EMAIL_CONFIRMATION": False,
    "ACTIVATION_URL": "auth/activation/{uid}/{token}",  # change to Frontend url
    "PASSWORD_RESET_CONFIRM_URL": "auth/password-reset/{uid}/{token}",  # change to Frontend url
    "LOGOUT_ON_PASSWORD_CHANGE": False,
    "TOKEN_LIFETIME": 3600,
    "SERIALIZERS": {
        "user_create": "account.serializers.UserCreateSerializer",
        "current_user": "account.serializers.UserSerializer",
    },
    "EMAIL": {
        "password_reset": "account.email.PasswordResetEmail",
        "activation": "account.email.ActivationEmail",
        "confirmation": "account.email.ConfirmationEmail",
        "password_changed_confirmation": "account.email.PasswordChangedConfirmationEmail",
    },
}

AUTH_USER_MODEL = os.getenv("AUTH_USER_MODEL")


ROOT_URLCONF = "Eshop.urls"

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

WSGI_APPLICATION = "Eshop.wsgi.application"


# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}


# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.postgresql',
#         'NAME': 'database_name',
#         'USER': 'database_user',
#         'PASSWORD': 'database_password',
#         'HOST': 'localhost',  # Or the hostname of your PostgreSQL server
#         'PORT': '5432',  # Default PostgreSQL port
#     }
# }


# Password validation
# https://docs.djangoproject.com/en/5.0/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/5.0/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.0/howto/static-files/

STATIC_URL = "static/"
STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles")


# Default primary key field type
# https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"


EMAIL_USE_TLS = True
EMAIL_USE_SSL = False

LOGIN_REDIRECT_URL = "/"


EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = "sandbox.smtp.mailtrap.io"
EMAIL_HOST_USER = os.getenv("EMAIL_HOST_USER")
EMAIL_HOST_PASSWORD = os.getenv("EMAIL_HOST_PASSWORD")
EMAIL_PORT = os.getenv("EMAIL_PORT")

# image storage configuration
CLOUDINARY_STORAGE = {
    "CLOUD_NAME": os.getenv("CLOUD_NAME"),
    "API_KEY": os.getenv("API_KEY"),
    "API_SECRET": os.getenv("API_SECRET"),
}

# add config
DEFAULT_FILE_STORAGE = "cloudinary_storage.storage.MediaCloudinaryStorage"

# celery configuration for task queuing. using reddis broker
CELERY_BROKER_URL = "redis://localhost:6379/0"
