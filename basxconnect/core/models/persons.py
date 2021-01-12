from bread.utils import get_concrete_instance, pretty_modelname
from django.contrib.contenttypes.fields import GenericRelation
from django.db import models
from django.utils.translation import gettext_lazy as _
from languages.fields import LanguageField
from simple_history.models import HistoricalRecords

from .. import settings
from .utils import Note, Term


class Person(models.Model):
    personnumber = models.CharField(
        _("Person number"), max_length=255, unique=True, blank=True
    )
    name = models.CharField(_("Display name"), max_length=255, blank=True)
    active = models.BooleanField(_("Active"), default=True)
    salutation_letter = models.CharField(
        _("Salutation Letter"),
        max_length=255,
        blank=True,
        help_text=_("e.g. Dear Mr. Smith, Hi Bob"),
    )
    preferred_language = LanguageField(
        _("Prefered Language"), blank=True, max_length=8
    )  # mitigate up-stream bug
    preferred_language.lazy_choices = (
        lambda field, request, instance: settings.PREFERRED_LANGUAGES
    )

    remarks = models.TextField(_("Remarks"), blank=True)
    notes = GenericRelation(Note)
    history = HistoricalRecords(inherit=True)

    def __str__(self):
        return self.name

    def type(self):
        return pretty_modelname(get_concrete_instance(self))

    type.verbose_name = _("Type")

    def status(self):
        return _("Active") if self.active else _("Inactive")

    status.verbose_name = _("Status")

    def address(self):
        return getattr(self.core_postal_list.first(), "address", "")

    address.verbose_name = _("Address")

    def postalcode(self):
        return getattr(self.core_postal_list.first(), "postcode", "")

    postalcode.verbose_name = _("Postal code")

    def city(self):
        return getattr(self.core_postal_list.first(), "city", "")

    city.verbose_name = _("City")

    def country(self):
        return getattr(self.core_postal_list.first(), "country", "")

    country.verbose_name = _("Country")

    def save(self, *args, **kwargs):
        if self.pk and not self.personnumber:
            self.personnumber = str(self.pk)
        super().save(*args, **kwargs)
        if not self.personnumber:
            self.personnumber = str(self.pk)
            super().save(*args, **kwargs)

    class Meta:
        ordering = ["name"]
        verbose_name = _("Person")
        verbose_name_plural = _("Persons")


class NaturalPerson(Person):
    first_name = models.CharField(_("First Name"), max_length=255, blank=True)
    middle_name = models.CharField(_("Middle Name"), max_length=255, blank=True)
    last_name = models.CharField(_("Last Name"), max_length=255, blank=True)
    title = models.ForeignKey(
        Term,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        limit_choices_to={"category__slug": "title"},
        related_name="title_persons",
    )
    salutation = models.ForeignKey(
        Term,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        limit_choices_to={"category__slug": "salutation"},
    )
    salutation.verbose_name = _("Salutation")
    title.verbose_name = _("Title")
    profession = models.CharField(
        _("Profession"),
        max_length=255,
        blank=True,
        help_text=_("e.g. Nurse, Carpenter"),
    )
    date_of_birth = models.DateField(_("Date of Birth"), blank=True, null=True)
    gender = models.ForeignKey(
        Term,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        limit_choices_to={"category__slug": "gender"},
        related_name="gender_persons",
    )
    gender.verbose_name = _("Gender")

    def save(self, *args, **kwargs):
        if not self.name:
            self.name = self.first_name + " " + self.last_name
        super().save(*args, **kwargs)

    class Meta:
        ordering = ["last_name", "first_name"]
        verbose_name = _("Natural Person")
        verbose_name_plural = _("Natural Persons")


class LegalPerson(Person):
    name_addition = models.CharField(_("Addition name"), max_length=255, blank=True)
    type = models.ForeignKey(
        Term,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        limit_choices_to={"category__slug": "legaltype"},
        help_text=_("eg. Church, Business, Association"),
    )
    type.verbose_name = _("Type")

    class Meta:
        ordering = ["name"]
        verbose_name = _("Legal Person")
        verbose_name_plural = _("Legal Persons")


class PersonAssociation(Person):
    class Meta:
        ordering = ["name"]
        verbose_name = _("Person Association")
        verbose_name_plural = _("Person Associations")
