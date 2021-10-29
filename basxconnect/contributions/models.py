import datetime

from django.conf import settings as djangosettings
from django.db import models
from django.utils.translation import gettext_lazy as _
from djmoney.contrib.exchange.models import convert_money
from djmoney.models.fields import CurrencyField
from djmoney.settings import CURRENCY_CHOICES
from dynamic_preferences.registries import global_preferences_registry
from moneyed import Money

from basxconnect.core.models import Person

from . import settings


class ContributionImport(models.Model):
    date = models.DateTimeField(_("Date"), default=datetime.datetime.now)
    importfile = models.FileField(_("Importfile"))
    user = models.ForeignKey(
        djangosettings.AUTH_USER_MODEL, null=True, on_delete=models.SET_NULL
    )
    user.verbose_name = _("User")

    def bookingrange(self):
        return f"{self.contributions.last().date} - {self.contributions.first().date}"

    bookingrange.verbose_name = _("Booking range")

    def numberofbookings(self):
        return self.contributions.count()

    numberofbookings.verbose_name = _("Number of bookings")

    def totalamount(self):
        global_preferences = global_preferences_registry.manager()
        return sum(
            [
                convert_money(
                    c.amount_formatted(), global_preferences["contributions__currency"]
                )
                for c in self.contributions.all()
            ]
        )

    totalamount.verbose_name = _("Total amount")

    def __str__(self):
        return f"{self.date.date()}"

    class Meta:
        verbose_name = _("Contribution Import")
        verbose_name_plural = _("Contributions Imports")
        ordering = ["-date"]


class Contribution(models.Model):
    _import = models.ForeignKey(
        ContributionImport,
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name="contributions",
    )
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
        ordering = ["-date"]
