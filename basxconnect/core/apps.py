from django import db
from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class CoreConfig(AppConfig):
    name = "basxconnect.core"
    default_auto_field = "django.db.models.BigAutoField"

    def ready(self):
        from .models import Vocabulary

        pre_installed_vocabulary = {
            "tag": _("Tags"),
            "title": _("Titles"),
            "salutation": _("Salutations"),
            "form_of_address": _("Forms Of Address"),
            "gender": _("Genders"),
            "naturaltype": _("Natural Person Types"),
            "legaltype": _("Legal Person Types"),
            "associationtype": _("Association Person Types"),
            "addressstatus": _("Address statuses"),
            "emailtype": _("Email Types"),
            "urltype": _("URL Types"),
            "phonetype": _("Phone Types"),
            "addresstype": _("Address Types"),
        }
        try:
            for slug, name in pre_installed_vocabulary.items():
                Vocabulary.objects.get_or_create(slug=slug, defaults={"name": name})
        except db.utils.OperationalError:
            pass
