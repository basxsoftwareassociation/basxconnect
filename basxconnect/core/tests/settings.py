# flake8: noqa
"""
For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.1/ref/settings/
"""

import os

from bread.settings.required import *

# the above will import a set of predefined settings to ensure required
# settings are defined correctly and to reduce verbosity in this file

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "test"  # nosec # can ignore security check for testing key

ALLOWED_HOSTS = ["*"]

# BREAD_DEPENDENCIES are imported in the start import at the top
INSTALLED_APPS = [
    "basxconnect.core.apps.CoreConfig",
    "basxconnect.contributions.apps.ContributionsConfig",
] + BREAD_DEPENDENCIES

TEMPLATES[0]["OPTIONS"]["context_processors"].append(
    "basxconnect.core.context_processors.basxconnect_core"
)

ROOT_URLCONF = "basxconnect.core.tests.urls"
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": ":memory:",
    }
}
HAYSTACK_CONNECTIONS = {
    "default": {
        "ENGINE": "haystack.backends.simple_backend.SimpleEngine",
    }
}
HAYSTACK_WHOOSH_STORAGE = "ram"
STATIC_URL = "static/"
STATIC_ROOT = "static"
