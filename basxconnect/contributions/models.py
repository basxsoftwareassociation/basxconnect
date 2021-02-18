import datetime

from django.db import models
from django.utils.translation import gettext_lazy as _
from djmoney.models.fields import CurrencyField
from djmoney.settings import CURRENCY_CHOICES
from moneyed import Money

from basxconnect.core.models import Person

from . import settings


class ContributionImport(models.Model):
    date = models.DateTimeField(default=datetime.datetime.now)
    importfile = models.FileField()

    def __str__(self):
        return f"{self.date.date()}"


class Contribution(models.Model):
    _import = models.ForeignKey(ContributionImport, null=True, on_delete=models.CASCADE)
    _import.verbose_name = _("Import")
    person = models.ForeignKey(
        Person, null=True, on_delete=models.SET_NULL, related_name="contributions"
    )
    person.verbose_name = _("Person")

    date = models.DateField(_("Date"))
    note = models.CharField(_("Note"), max_length=255)
    debitaccount = models.CharField(_("Debit Account"), max_length=32)
    creditaccount = models.CharField(_("Credit Account"), max_length=32)
    amount = models.DecimalField(_("Amount"), max_digits=12, decimal_places=2)
    currency = CurrencyField(_("Currency"), choices=CURRENCY_CHOICES)
    currency.lazy_choices = lambda *args: settings.PREFERRED_CURRENCIES

    def amount_formatted(self):
        return Money(self.amount, self.currency)

    amount_formatted.verbose_name = _("Amount")

    def __str__(self):
        return f"{self.date}: {self.person} {self.amount_formatted()}"

    class Meta:
        verbose_name = _("Contribution")
        verbose_name_plural = _("Contributions")
