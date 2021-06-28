from django.conf import settings
from languages.languages import LANGUAGES

DEFAULTS = {"PREFERRED_LANGUAGES": ("en",), "OWNER_PERSON_ID": 1}

preferred_codes = getattr(settings, "BASXCONNECT", {}).get(
    "PREFERRED_LANGUAGES", DEFAULTS["PREFERRED_LANGUAGES"]
)
PREFERRED_LANGUAGES = [i for i in LANGUAGES if i[0] in preferred_codes]
PREFERRED_LANGUAGES.sort(key=lambda e: preferred_codes.index(e[0]))

OWNER_PERSON_ID = getattr(settings, "BASXCONNECT", {}).get(
    "OWNER_PERSON_ID", DEFAULTS["OWNER_PERSON_ID"]
)

ENABLE_CONTRIBUTIONS = False
MIN_CHARACTERS_DYNAMIC_SEARCH = getattr(settings, "MIN_CHARACTERS_DYNAMIC_SEARCH", 3)
