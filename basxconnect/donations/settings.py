from django.conf import settings
from djmoney.settings import CURRENCY_CHOICES

DEFAULTS = {"PREFERRED_CURRENCIES": [i for i in CURRENCY_CHOICES if i[0] == "USD"]}

PREFERRED_CURRENCIES = getattr(settings, "BASXCONNECT", DEFAULTS)[
    "PREFERRED_CURRENCIES"
]
