from basxconnect.core.models import Person
from django.db import models
from django.utils.translation import gettext_lazy as _
from djmoney.models.fields import CurrencyField
from djmoney.settings import CURRENCY_CHOICES

from . import settings


class DonationImport(models.Model):
    date = models.DateTimeField()


class Donation(models.Model):
    _import = models.ForeignKey(DonationImport, null=True, on_delete=models.CASCADE)
    _import.verbose_name = _("Import")
    person = models.ForeignKey(
        Person, null=True, on_delete=models.SET_NULL, related_name="donations"
    )
    person.verbose_name = _("Person")
    amount = models.DecimalField(_("Amount"), max_digits=12, decimal_places=2)
    currency = CurrencyField(_("Currency"), choices=CURRENCY_CHOICES)
    currency.lazy_choices = lambda *args: settings.PREFERRED_CURRENCIES
    date = models.DateField(_("Date"))

    class Meta:
        verbose_name = _("Donation")
        verbose_name_plural = _("Donations")
