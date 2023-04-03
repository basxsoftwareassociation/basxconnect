from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class InvoicingConfig(AppConfig):
    name = "basxconnect.invoicing"
    label = "basxconnect_invoicing"
    default_auto_field = "django.db.models.BigAutoField"
    verbose_name = _("BasxConnect Invoicing")
