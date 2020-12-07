from django import forms
from django.utils.translation import gettext_lazy as _
from dynamic_preferences.preferences import Section
from dynamic_preferences.registries import global_preferences_registry
from dynamic_preferences.types import FilePreference, LongStringPreference

general = Section("general", _("General"))


@global_preferences_registry.register
class SenderLetterhead(LongStringPreference):
    section = general
    name = "sender_letterhead"
    default = ""
    verbose_name = _("Sender letterhead")


@global_preferences_registry.register
class Logo(FilePreference):
    section = general
    name = "logo"
    field_class = forms.ImageField
    default = ""
    verbose_name = _("Logo")

    field_kwargs = {
        "required": False,
    }
