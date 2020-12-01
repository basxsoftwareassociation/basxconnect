# flake8: noqa
"""
For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.1/ref/settings/
"""

import os

from bread.settings.required import *

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
PROJECT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASE_DIR = os.path.dirname(PROJECT_DIR)


# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "c=c1lb*h^61l9awqoimi_kp2q=%kpz1r$hz)j9+hq+mm^njsn^"

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = ["core"] + BREAD_DEPENDENCIES

ROOT_URLCONF = "basxconnect.urls"

WSGI_APPLICATION = "wsgi.application"

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": os.path.join(BASE_DIR, "db.sqlite3"),
    }
}

HAYSTACK_CONNECTIONS = {
    "default": {
        "ENGINE": "haystack.backends.whoosh_backend.WhooshEngine",
        "PATH": os.path.join(BASE_DIR, "woosh_index"),
    },
}

STATIC_ROOT = os.path.join(BASE_DIR, "static")
STATIC_URL = "/static/"

MEDIA_ROOT = os.path.join(BASE_DIR, "media")
MEDIA_URL = "/media/"

LOCALE_PATHS = ["locale"]
