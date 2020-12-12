import os
from pathlib import Path

import dj_database_url

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve(strict=True).parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
# SECRET_KEY = '74fwmy8oo0@p%&2z1e&lsg=qxq1022x!(1^6du-r@w#&jf9!9n'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
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

ROOT_URLCONF = "copasfn.urls"

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

WSGI_APPLICATION = "copasfn.wsgi.application"


# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}


# Password validation
# https://docs.djangoproject.com/en/3.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]


# Internationalization
# https://docs.djangoproject.com/en/3.1/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.1/howto/static-files/

STATIC_URL = "/static/"


#
# Custom settings
#

AUTH_USER_MODEL = "costos.Profesional"

# Internationalization

LANGUAGE_CODE = "es-ar"
TIME_ZONE = "America/Buenos_Aires"
USE_THOUSAND_SEPARATOR = True

# Applications

APPS_BEFORE = [
    # my applications
]
APPS_AFTER = [
    # my applications
    "costos.apps.CostosConfig",
    # other applications
    "dynamic_preferences",
    # comment the following line if you don't want to use user preferences
    "dynamic_preferences.users.apps.UserPreferencesConfig",
    "rest_framework",
    "django_extensions",
    "crispy_forms",
    "captcha",
]
# Apps installed before have priority
INSTALLED_APPS = APPS_BEFORE + INSTALLED_APPS + APPS_AFTER

# Middleware

# add whitenoise just after SecurityMiddleware
sm_index = MIDDLEWARE.index("django.middleware.security.SecurityMiddleware")
MIDDLEWARE.insert(sm_index + 1, "whitenoise.middleware.WhiteNoiseMiddleware")

# Templates

TEMPLATES[0]["DIRS"].append(BASE_DIR / "templates")

# Deployment

# Heroku
HEROKUAPP_NAME = os.environ.get("DJANGO_HEROKUAPP_NAME", "copasfn")
SECRET_KEY = os.environ.get("DJANGO_SECRET_KEY", "r+)1xlbz%lau$zpv$mbn#_6cy6rkc-eg!2@0s45jx!2ubuo3m1")
DEBUG = os.environ.get("DJANGO_DEBUG", "") != "False"
CUSTOM_DOMAIN_NAME = os.environ.get("CUSTOM_DOMAIN_NAME", "")
ALLOWED_HOSTS = [
    "127.0.0.1",
    f"{HEROKUAPP_NAME}.herokuapp.com",
    CUSTOM_DOMAIN_NAME,
]

# Redirect to home URL after login (Default redirects to /accounts/profile/)
LOGIN_REDIRECT_URL = "/"

# Mail sending / default value is smtp
EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
# EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"

# SendGrid
DEFAULT_FROM_EMAIL = os.environ.get("DJANGO_DEFAULT_FROM_EMAIL")
SENDGRID_API_KEY = os.environ.get("SENDGRID_API_KEY")
EMAIL_HOST = "smtp.sendgrid.net"
EMAIL_HOST_USER = "apikey"  # this is exactly the value 'apikey'
EMAIL_HOST_PASSWORD = SENDGRID_API_KEY
EMAIL_PORT = 587
EMAIL_USE_TLS = True

# Heroku: Update DATABASE configuration from $DATABASE_URL.
db_from_env = dj_database_url.config(conn_max_age=500)
DATABASES["default"].update(db_from_env)

# Static files

# The list of folders where Django will search for additional static files aside from the static folder of each app installed.
STATICFILES_DIRS = [
    BASE_DIR / "static",
]

# The absolute path to the directory where collectstatic will collect static files for deployment.
STATIC_ROOT = BASE_DIR / "staticfiles"

# Simplified static file serving.
# https://warehouse.python.org/project/whitenoise/
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

# Crispy Forms
CRISPY_TEMPLATE_PACK = "bootstrap4"

# reCAPTCHA
RECAPTCHA_PUBLIC_KEY = os.environ.get("RECAPTCHA_PUBLIC_KEY", "6LdB_wAaAAAAAErHBvEgeTC16AY3bow9zP2vbE9T")
RECAPTCHA_PRIVATE_KEY = os.environ.get("RECAPTCHA_PRIVATE_KEY", "")
RECAPTCHA_REQUIRED_SCORE = os.environ.get("RECAPTCHA_REQUIRED_SCORE", 0.75)

# Dynamic Preferences
TEMPLATES[0]["OPTIONS"]["context_processors"].append("dynamic_preferences.processors.global_preferences")

# Logging
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
        },
    },
    "loggers": {
        "django": {
            "handlers": ["console"],
            "level": os.getenv("DJANGO_LOG_LEVEL", "DEBUG"),
        },
    },
}
