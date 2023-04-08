import datetime
import decimal
import re

import htmlgenerator as hg
from basxbread import utils
from django.db import models
from django.utils.translation import gettext_lazy as _
from djmoney.money import Money
from djmoney.settings import CURRENCY_CHOICES
from dynamic_preferences.registries import global_preferences_registry

from basxconnect.core.models import Person
from basxconnect.projects.models import Project


def pref(name, section="invoicing"):
    global_preferences = global_preferences_registry.manager()
    return global_preferences[f"{section}__{name}"]


class PaymentType(models.Model):
    name = models.CharField(
        _("Name"), max_length=255, help_text=_("Internal name of this payment method")
    )
    payment_information = models.TextField(
        _("Payment information"),
        help_text=_("Instructions for the client"),
    )

    def __str__(self):
        return self.name

    class Meta:
        ordering = ["name"]
        verbose_name = _("Payment type")
        verbose_name_plural = _("Payment types")


class InvoiceManager(models.Manager):
    def get_active(self):
        return super().get_queryset().filter(cancelled=None)

    def get_cancelled(self):
        return super().get_queryset().exclude(cancelled=None)


def default_invoice_number():
    counts = {}
    group_regex = re.compile(pref("invoice_number_grouping_regex"))
    counter_regex = re.compile(pref("invoice_number_extraction_regex"))
    for invoice in Invoice.objects.all():
        group_match = group_regex.match(getattr(invoice, "number", ""))
        counter_match = counter_regex.match(getattr(invoice, "number", ""))
        if group_match is not None and counter_match is not None:
            group = group_match.groups()[0]
            if group not in counts:
                counts[group] = 0
            try:
                counts[group] = max(int(counter_match.groups()[0]), counts[group])
            except ValueError:
                pass

    counter_next = 1
    tmp_value = utils.jinja_render(pref("invoice_number_template"), counter_next=0)
    group_match = group_regex.match(tmp_value)
    if group_match is not None:
        counter_next = counts.get(group_match.groups()[0], 0) + 1
    return utils.jinja_render(
        pref("invoice_number_template"), counter_next=counter_next
    )


def default_currency():
    return pref("default_currency")


def default_include_vat():
    return pref("amounts_include_vat")


def default_vat():
    if pref("default_use_vat") is False:
        return decimal.Decimal(0)
    return pref("default_vat")


def default_wht():
    if pref("default_use_wht") is False:
        return decimal.Decimal(0)
    return pref("default_wht")


class Invoice(models.Model):
    number = models.CharField(
        _("Invoice number"), max_length=255, default=default_invoice_number, unique=True
    )
    client = models.ForeignKey(
        Person,
        on_delete=models.CASCADE,
        related_name="invoices",
        verbose_name=_("Client"),
    )
    currency = models.CharField(
        _("Currency"), max_length=3, choices=CURRENCY_CHOICES, default=default_currency
    )
    paymenttype = models.ForeignKey(
        PaymentType,
        null=True,
        on_delete=models.SET_NULL,
        verbose_name=PaymentType._meta.verbose_name,
    )
    created = models.DateField(_("Created on"), default=datetime.date.today)
    payed = models.DateField(_("Payed on"), null=True, blank=True)
    invoice_sent = models.DateField(_("Invoice sent"), null=True, blank=True)
    receipt_sent = models.DateField(_("Receipt sent"), null=True, blank=True)
    cancelled = models.DateField(_("Cancelled"), null=True, blank=True)
    note = models.TextField(
        _("Note to client"),
        blank=True,
        help_text=_("Can be displayed on invoice and/or receipt"),
    )

    # tax related
    amounts_include_vat = models.BooleanField(
        _("Amounts include VAT"), default=default_include_vat
    )
    vat = models.DecimalField(
        _("VAT"), max_digits=4, decimal_places=3, default=default_vat
    )
    wht = models.DecimalField(
        _("WHT"), max_digits=4, decimal_places=3, default=default_wht
    )

    objects = InvoiceManager()

    def has_vat(self):
        return self.vat > 0

    has_vat.verbose_name = _("Has VAT")

    def has_wht(self):
        return self.wht > 0

    has_wht.verbose_name = _("Has WHT")

    def net_amount(self):
        net_multiply = 1
        if self.amounts_include_vat:
            net_multiply += self.vat
        amount = sum(i.amount / net_multiply for i in self.items.all())
        return Money(amount, self.currency)

    net_amount.verbose_name = _("Net amount")

    def vat_amount(self):
        return self.net_amount() * self.vat

    vat_amount.verbose_name = _("VAT amount")

    def wht_amount(self):
        return self.net_amount() * self.wht

    wht_amount.verbose_name = _("WHT amount")

    def total_amount(self):
        return (self.net_amount() + self.vat_amount()) - self.wht_amount()

    total_amount.verbose_name = _("Total amount")

    def __html__(self):
        if self.cancelled:
            return hg.SPAN(
                f"{self._meta.verbose_name} {self.number} ({self.client})",
                style="text-decoration: line-through;",
            )
        return f"{self._meta.verbose_name} {self.number} ({self.client})"

    def __str__(self):
        if self.cancelled:
            return f"{self._meta.verbose_name} {self.number} (_('Cancelled'))"
        return f"{self._meta.verbose_name} {self.number}"

    class Meta:
        ordering = ["-created", "-id"]
        verbose_name = _("Invoice")
        verbose_name_plural = _("Invoices")


def project_choices(field, request, instance):
    if instance is None or instance.client is None:
        return []
    return instance.client.projects.all()


class Item(models.Model):
    invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE, related_name="items")
    amount = models.DecimalField(max_digits=14, decimal_places=2)
    description = models.CharField(max_length=1024)
    project = models.ForeignKey(
        Project,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="invoices",
        verbose_name=Project._meta.verbose_name,
    )
    project.lazy_choices = project_choices

    def amount_with_currency(self):
        return Money(self.amount, self.invoice.currency)

    def __str__(self):
        return f"{self.description}: {Money(self.amount, self.invoice.currency)}: "

    class Meta:
        verbose_name = _("Item")
        verbose_name_plural = _("Items")
