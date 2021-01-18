from basxconnect.core.models import Person
from django.db import models
from djmoney.models.fields import CurrencyField
from djmoney.settings import CURRENCY_CHOICES

from . import settings


class DonationImport(models.Model):
    date = models.DateTimeField()


class Donation(models.Model):
    _import = models.ForeignKey(DonationImport, null=True, on_delete=models.CASCADE)
    person = models.ForeignKey(Person, null=True, on_delete=models.SET_NULL)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    currency = CurrencyField(choices=CURRENCY_CHOICES)
    currency.lazy_choices = lambda *args: settings.PREFERRED_CURRENCIES
    date = models.DateField()
