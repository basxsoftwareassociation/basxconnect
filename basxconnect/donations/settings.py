from django.conf import settings
from djmoney.settings import CURRENCY_CHOICES

DEFAULTS = {"PREFERRED_CURRENCIES": [i for i in CURRENCY_CHOICES if i[0] == "USD"]}

preferred_codes = getattr(settings, "BASXCONNECT", {}).get(
    "PREFERRED_CURRENCIES", DEFAULTS["PREFERRED_CURRENCIES"]
)
PREFERRED_CURRENCIES = [i for i in CURRENCY_CHOICES if i[0] in preferred_codes]
PREFERRED_CURRENCIES.sort(key=lambda e: preferred_codes.index(e[0]))
