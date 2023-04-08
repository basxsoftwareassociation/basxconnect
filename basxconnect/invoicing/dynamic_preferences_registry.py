import decimal
import re

import htmlgenerator as hg
from basxbread.contrib.document_templates.models import DocumentTemplate
from django.forms import ValidationError
from django.utils.translation import gettext_lazy as _
from djmoney import settings
from dynamic_preferences.preferences import Section
from dynamic_preferences.registries import global_preferences_registry
from dynamic_preferences.types import (
    BooleanPreference,
    ChoicePreference,
    DecimalPreference,
    LongStringPreference,
    ModelChoicePreference,
    StringPreference,
)

from basxconnect.core.models import Term

invoicing = Section("invoicing", _("Invoicing"))


@global_preferences_registry.register
class DefaultCurrency(ChoicePreference):
    section = invoicing
    name = "default_currency"
    verbose_name = _("Default currency")
    default = settings.DEFAULT_CURRENCY or "EUR"
    choices = settings.CURRENCY_CHOICES


@global_preferences_registry.register
class UseVAT(BooleanPreference):
    section = invoicing
    name = "default_use_vat"
    verbose_name = _("Use VAT by default")
    default = True


@global_preferences_registry.register
class DefaultVAT(DecimalPreference):
    section = invoicing
    name = "default_vat"
    verbose_name = _("Default VAT")
    default = decimal.Decimal(0)


@global_preferences_registry.register
class UseWHT(BooleanPreference):
    section = invoicing
    name = "default_use_wht"
    verbose_name = _("Use WHT by default")
    default = False


@global_preferences_registry.register
class DefaultWHT(DecimalPreference):
    section = invoicing
    name = "default_wht"
    verbose_name = _("Default WHT")
    default = decimal.Decimal(0)


@global_preferences_registry.register
class AmountsIncludeVAT(BooleanPreference):
    section = invoicing
    name = "amounts_include_vat"
    verbose_name = _("Provided invoicing amounts include VAT by default")
    default = False


@global_preferences_registry.register
class InvoiceNumberGroupingRegex(StringPreference):
    section = invoicing
    name = "invoice_number_grouping_regex"
    verbose_name = _("Invoice number grouping regex")
    help_text = hg.UL(
        "Regex with exactly one group that extracts a grouping value for invoices"
    )
    default = r"(.*)-.*"

    def validate(self, value):
        try:
            groups = re.compile(value).groups
            if groups != 1:
                raise ValidationError(
                    "Requires exactly one regex group, found {groups}"
                )
        except Exception as e:
            raise ValidationError(str(e))


@global_preferences_registry.register
class InvoiceNumberExtractionRegex(StringPreference):
    section = invoicing
    name = "invoice_number_extraction_regex"
    verbose_name = _("Invoice number extraction regex")
    help_text = hg.UL("Regex with exactly one group that extracts a integer value")
    default = r".*-(\d*)"

    def validate(self, value):
        try:
            groups = re.compile(value).groups
            if groups != 1:
                raise ValidationError(
                    "Requires exactly one regex group, found {groups}"
                )
        except Exception as e:
            raise ValidationError(str(e))


@global_preferences_registry.register
class InvoiceNumberTemplate(StringPreference):
    section = invoicing
    name = "invoice_number_template"
    verbose_name = _("Invoice number template")
    help_text = hg.UL(
        hg.LI("Jinja template to generate invoice number"),
        hg.LI("Context variable 'date': current date"),
        hg.LI(
            "Context variable 'counter_next': Next counter number (depending on counter extraction regex)"
        ),
    )
    default = "{{ now()|date('Y') }}-{{ counter_next }}"


@global_preferences_registry.register
class DefaultInvoiceTemplate(ModelChoicePreference):
    section = invoicing
    name = "default_invoice_template"
    verbose_name = _("Default invoice template")
    queryset = DocumentTemplate.objects.filter(
        model__app_label="basxconnect_invoicing", model__model="invoice"
    )
    default = None


@global_preferences_registry.register
class DefaultReceiptTemplate(ModelChoicePreference):
    section = invoicing
    name = "default_receipt_template"
    verbose_name = _("Default receipt template")
    queryset = DocumentTemplate.objects.filter(
        model__app_label="basxconnect_invoicing", model__model="invoice"
    )
    default = None


@global_preferences_registry.register
class InvoiceEmailSubject(StringPreference):
    section = invoicing
    name = "invoice_message_subject_template"
    verbose_name = _("Invoice email subject")
    help_text = hg.UL(
        hg.LI("Jinja template to generate invoice email subject"),
        hg.LI("Context variable 'invoice'"),
        hg.LI("Context variable 'our_company_name'"),
    )
    default = "Invoice {{ invoice.number }} from {{ our_company_name }}"


@global_preferences_registry.register
class InvoiceEmailBody(LongStringPreference):
    section = invoicing
    name = "invoice_message_body_template"
    verbose_name = _("Invoice email body")
    help_text = hg.UL(
        hg.LI("Jinja template to generate invoice email body"),
        hg.LI("Context variable 'invoice'"),
        hg.LI("Context variable 'our_company_name'"),
    )
    default = """Hi {{ invoice.client }}

This is the latest invoice for our services, please find it attached to this message.

Have a nice day!"""


@global_preferences_registry.register
class DefaultInvoiceEmail(ModelChoicePreference):
    section = invoicing
    name = "default_invoice_email_type"
    queryset = Term.objects.filter(vocabulary__slug="emailtype")
    verbose_name = _("Default invoice email")
    default = None


@global_preferences_registry.register
class ReceiptEmailSubject(StringPreference):
    section = invoicing
    name = "receipt_message_subject_template"
    verbose_name = _("Receipt email subject")
    help_text = hg.UL(
        hg.LI("Jinja template to generate receipt email subject"),
        hg.LI("Context variable 'invoice'"),
        hg.LI("Context variable 'our_company_name'"),
    )
    default = "Receipt for invoice {{ invoice.number }} from {{ our_company_name }}"


@global_preferences_registry.register
class ReceiptEmailBody(LongStringPreference):
    section = invoicing
    name = "receipt_message_body_template"
    verbose_name = _("Receipt email body")
    help_text = hg.UL(
        hg.LI("Jinja template to generate receipt email body"),
        hg.LI("Context variable 'invoice'"),
        hg.LI("Context variable 'our_company_name'"),
    )
    default = """Hi {{ invoice.client }}

This is the receipt for invoice {{ invoice.number }}, please find it in the attachment.

Have a nice day!"""
