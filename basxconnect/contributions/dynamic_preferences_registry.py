from django.utils.translation import gettext_lazy as _
from djmoney.settings import CURRENCY_CHOICES
from dynamic_preferences.preferences import Section
from dynamic_preferences.registries import global_preferences_registry
from dynamic_preferences.types import ChoicePreference

contributions = Section("contributions", _("Contributions"))


@global_preferences_registry.register
class PreferredCurrency(ChoicePreference):
    section = contributions
    name = "currency"
    default = "EUR"
    verbose_name = _("Preferred Currency")
    choices = CURRENCY_CHOICES
