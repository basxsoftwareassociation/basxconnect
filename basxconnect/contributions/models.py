from django.db import models
from django.utils.translation import gettext_lazy as _
from djmoney.models.fields import CurrencyField
from djmoney.settings import CURRENCY_CHOICES

from basxconnect.core.models import Person

from . import settings


class ContributionImport(models.Model):
    date = models.DateTimeField()


class Contribution(models.Model):
    _import = models.ForeignKey(ContributionImport, null=True, on_delete=models.CASCADE)
    _import.verbose_name = _("Import")
    person = models.ForeignKey(
        Person, null=True, on_delete=models.SET_NULL, related_name="contributions"
    )
    person.verbose_name = _("Person")

    date = models.DateField(_("Date"))
    note = models.CharField(_("Note"), max_length=255)
    account = models.CharField(_("Account"), max_length=32)
    cost_center = models.CharField(_("Cost center"), max_length=32)
    amount = models.DecimalField(_("Amount"), max_digits=12, decimal_places=2)
    currency = CurrencyField(_("Currency"), choices=CURRENCY_CHOICES)
    currency.lazy_choices = lambda *args: settings.PREFERRED_CURRENCIES

    class Meta:
        verbose_name = _("Contribution")
        verbose_name_plural = _("Contributions")
