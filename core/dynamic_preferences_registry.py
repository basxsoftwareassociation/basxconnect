from django import forms
from dynamic_preferences.preferences import Section
from dynamic_preferences.registries import global_preferences_registry
from dynamic_preferences.types import FilePreference, LongStringPreference

general = Section("general")


@global_preferences_registry.register
class SenderLetterhead(LongStringPreference):
    section = general
    name = "sender_letterhead"
    default = ""


@global_preferences_registry.register
class Logo(FilePreference):
    section = general
    name = "logo"
    field_class = forms.ImageField
    default = ""

    field_kwargs = {
        "required": False,
    }
