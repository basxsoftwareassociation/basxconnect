from django import forms
from django.utils.translation import gettext_lazy as _
from dynamic_preferences.preferences import Section
from dynamic_preferences.registries import global_preferences_registry
from dynamic_preferences.types import (
    FilePreference,
    LongStringPreference,
    ModelChoicePreference,
    StringPreference,
)

from basxconnect.core.models import Term

general = Section("general", _("General"))
persons = Section("persons", _("Persons"))


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


@global_preferences_registry.register
class OrganizationName(StringPreference):
    section = general
    name = "organizationname"
    default = "<Your Organization>"
    verbose_name = _("Organization Name")


@global_preferences_registry.register
class DefaultTypeNaturalPerson(ModelChoicePreference):
    section = persons
    name = "default_naturaltype"
    default = None
    queryset = Term.objects.filter(vocabulary__slug="naturaltype")
    verbose_name = _("Default type of natural persons")


@global_preferences_registry.register
class DefaultTypePersonAssociation(ModelChoicePreference):
    section = persons
    name = "default_associationtype"
    default = None
    queryset = Term.objects.filter(vocabulary__slug="associationtype")
    verbose_name = _("Default type of person associations")


@global_preferences_registry.register
class DefaultTypeLegalPerson(ModelChoicePreference):
    section = persons
    name = "default_legaltype"
    default = None
    queryset = Term.objects.filter(vocabulary__slug="legaltype")
    verbose_name = _("Default type of legal persons")
