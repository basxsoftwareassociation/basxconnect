from django.db import models
from django.utils.translation import gettext_lazy as _
from languages.fields import LanguageField

from .utils import Term


class Person(models.Model):
    created = models.DateField(_("Created"), editable=False, auto_now_add=True)
    name = models.CharField(_("Name"), max_length=255)
    deleted = models.BooleanField(_("Deleted"), default=False)
    salutation = models.ForeignKey(
        Term,
        on_delete=models.SET_NULL,
        null=True,
        limit_choices_to={"category__slug": "salutation"},
    )
    salutation.verbose_name = _("Salutation")
    salutation_letter = models.CharField(
        _("Salutation Letter"),
        max_length=255,
        blank=True,
        help_text=_("e.g. Dear Mr. Smith, Hi Bob"),
    )
    preferred_language = LanguageField(_("Prefered Language"), blank=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ["name"]


class NaturalPerson(Person):
    first_name = models.CharField(_("First Name"), max_length=255)
    middle_name = models.CharField(_("Middle Name"), max_length=255, blank=True)
    last_name = models.CharField(_("Last Name"), max_length=255)
    title = models.ForeignKey(
        Term,
        on_delete=models.SET_NULL,
        null=True,
        limit_choices_to={"category__slug": "title"},
        related_name="title_persons",
    )
    title.verbose_name = _("Title")
    profession = models.CharField(
        _("Profession"),
        max_length=255,
        blank=True,
        help_text=_("e.g. Nurse, Carpenter"),
    )
    date_of_birth = models.DateField(_("Date of Birth"), null=True)
    gender = models.ForeignKey(
        Term,
        on_delete=models.SET_NULL,
        null=True,
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


class JuristicPerson(Person):
    type = models.ForeignKey(
        Term,
        on_delete=models.SET_NULL,
        null=True,
        limit_choices_to={"category__slug": "legaltype"},
        help_text=_("eg. Church, Business, Association"),
    )
    type.verbose_name = _("Type")

    class Meta:
        ordering = ["name"]
        verbose_name = _("Juristic Person")
        verbose_name_plural = _("Juristic Persons")


class PersonAssociation(Person):
    class Meta:
        ordering = ["name"]
        verbose_name = _("Person Association")
        verbose_name_plural = _("Person Associations")
