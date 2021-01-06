from django.conf import settings

DEFAULTS = {"PREFERRED_LANGUAGES": (("en", "English"),)}

PREFERRED_LANGUAGES = getattr(settings, "BASXCONNECT", DEFAULTS)["PREFERRED_LANGUAGES"]
