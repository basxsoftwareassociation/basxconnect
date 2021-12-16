import datetime
import random

from bread import layout
from bread.contrib.languages.fields import LanguageField
from bread.utils import get_concrete_instance, pretty_modelname
from bread.utils.inheritancemanager import InheritanceManager
from django.contrib.contenttypes.fields import GenericRelation
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from dynamic_preferences.registries import global_preferences_registry
from simple_history.models import HistoricalRecords

from .utils import Note, Term


def preferred_languages_choices(field, request, instance):
    from .. import settings

    return settings.PREFERRED_LANGUAGES


class PersonManager(InheritanceManager):
    def get_queryset(self):
        return super().get_queryset().select_subclasses()

    def trash(self, *args, **kwargs):
        return super().get_queryset(*args, **kwargs).filter(deleted=True)

    def not_deleted(self, *args, **kwargs):
        return super().get_queryset(*args, **kwargs).filter(deleted=False)


# don't delete this function, other initial migrations for new projects will fail
def random_personid():
    # this is not security related, we can disable checks here
    return f"__placeholder__{random.randint(100000, 999999)}"  # nosec


class Person(models.Model):
    deleted = models.BooleanField(_("Deleted"), blank=True, default=False)
    personnumber = models.CharField(
        _("Person number"),
        max_length=255,
        unique=True,
        default=random_personid,
    )
    personnumber.sorting_name = "personnumber__int"
    name = models.CharField(_("Display name"), max_length=255, blank=True)
    # this one is to solve a problem when sorting names from
    # naturalperson and other types of person
    default_sorting_name = models.CharField(
        _("Default Sorting Name"), max_length=255, blank=True
    )
    active = models.BooleanField(_("Active"), default=True)
    salutation_letter = models.CharField(
        _("Salutation Letter"),
        max_length=255,
        blank=True,
    )
    preferred_language = LanguageField(_("Preferred Language"), blank=True)
    preferred_language.lazy_choices = preferred_languages_choices

    tags = models.ManyToManyField(
        Term,
        blank=True,
        limit_choices_to={"vocabulary__slug": "tag"},
        # db_table="core_person_categories",
    )
    tags.verbose_name = _("Tags")

    primary_postal_address = models.ForeignKey(
        "core.Postal",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="primary_address_for",
    )
    primary_postal_address.verbose_name = _("Primary postal address")
    primary_postal_address.lazy_choices = (
        lambda field, request, instance: instance.core_postal_list.all()
        if hasattr(instance, "core_postal_list")
        else None
    )
    primary_email_address = models.ForeignKey(
        "core.Email",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="primary_email_for",
    )
    primary_email_address.verbose_name = _("Primary email address")
    primary_email_address.lazy_choices = (
        lambda field, request, instance: instance.core_email_list.all()
        if hasattr(instance, "core_email_list")
        else None
    )

    remarks = models.TextField(_("Remarks"), blank=True)
    notes = GenericRelation(Note)
    history = HistoricalRecords(inherit=True)
    _maintype = models.CharField(  # only used internally for filtering or sorting
        max_length=32,
        choices=(
            ("person", "person"),
            ("naturalperson", "naturalperson"),
            ("legalperson", "legalperson"),
            ("personassociation", "personassociation"),
        ),
        editable=False,
    )

    _type = models.ForeignKey(
        Term, on_delete=models.SET_NULL, null=True, blank=True, related_name="+"
    )
    _type.verbose_name = _("Person Type")

    objects = PersonManager()

    def __str__(self):
        return self.name

    def maintype(self):
        return pretty_modelname(get_concrete_instance(self))

    maintype.verbose_name = _("Main Type")
    maintype.sorting_name = "_maintype"

    def status(self):
        return (
            layout.tag.Tag(_("active"), tag_color="green")
            if self.active
            else layout.tag.Tag(_("inactive"), tag_color="red")
        )

    status.verbose_name = _("Status")
    status.sorting_name = "active"

    def save(self, *args, **kwargs):
        created = self.pk is None
        # automatically generate a person number if empty
        # if this object is just beeing create we do not have
        # a person number (because there is no pk) and we need
        # to do the same thing again after a call to super.save
        # and then save again
        # the random-things is a bit ugly but if we want to enforce uniqueness
        # on the database level we have to use this one during creation

        if not self._maintype:
            self._maintype = "person"
        if hasattr(self, "core_postal_list"):
            active_postals = [
                postal
                for postal in self.core_postal_list.all()
                if postal.valid_until is None
                or postal.valid_until >= timezone.now().date()
            ]
            if len(active_postals) == 0:
                self.primary_postal_address = None
            elif (
                len(active_postals) == 1
                or self.primary_postal_address is None
                or (
                    self.primary_postal_address.valid_until
                    and self.primary_postal_address.valid_until < timezone.now().date()
                )
            ):
                self.primary_postal_address = active_postals[0]

        else:
            self.primary_postal_address = None
        if hasattr(self, "core_email_list"):
            if (
                self.core_email_list.all().count() == 1
                or self.primary_email_address is None
            ):
                self.primary_email_address = self.core_email_list.first()
        else:
            self.primary_email_address = None

        super().save(*args, **kwargs)
        if self.personnumber.startswith("__placeholder__"):
            self.personnumber = str(self.pk)
            super().save(update_fields=["personnumber"])

        self.default_sorting_name = self.name

        # this signal needs to be sent manually in order to trigger the search-index update
        # Django does only send a signal for the child-model but our search-index only observes
        # this base model. It is only needed when creating for some reason...
        models.signals.post_save.send(
            sender=Person,
            instance=getattr(self, "person_ptr", self),
            created=created,
            update_fields=kwargs.get("update_fields"),
            raw=False,
            using=kwargs.get("using"),
        )

    def search_index_snippet(self):
        concrete = get_concrete_instance(self)
        if concrete != self and hasattr(concrete, "search_index_snippet"):
            return concrete.search_index_snippet()
        addr = self.primary_postal_address
        pieces = [self.name]
        if addr:
            pieces.append(addr.address.replace("\n", " "))
            pieces.append(f"{addr.postcode} {addr.city}")
            pieces.append(addr.country.code)

        return ", ".join(pieces)

    class Meta:
        ordering = ["name"]
        verbose_name = _("Person")
        verbose_name_plural = _("Persons")


class NaturalPerson(Person):
    first_name = models.CharField(_("First Name"), max_length=255, blank=True)
    middle_name = models.CharField(_("Middle Name"), max_length=255, blank=True)
    last_name = models.CharField(_("Last Name"), max_length=255, blank=True)
    autogenerate_displayname = models.BooleanField(
        _("Autogenerate Display Name"), default=True
    )
    title = models.ForeignKey(
        Term,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        limit_choices_to={"vocabulary__slug": "title"},
        related_name="title_persons",
    )
    title.verbose_name = _("Title")
    salutation = models.ForeignKey(
        Term,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        limit_choices_to={"vocabulary__slug": "salutation"},
        related_name="+",
    )
    salutation.verbose_name = _("Salutation")

    form_of_address = models.ForeignKey(
        Term,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        limit_choices_to={"vocabulary__slug": "form_of_address"},
        related_name="+",
    )
    form_of_address.verbose_name = _("Form of address")

    profession = models.CharField(
        _("Profession"),
        max_length=255,
        blank=True,
    )
    date_of_birth = models.DateField(_("Date of Birth"), blank=True, null=True)
    deceased = models.BooleanField(_("Deceased"), default=False)
    decease_date = models.DateField(_("Deceased Date"), blank=True, null=True)
    gender = models.ForeignKey(
        Term,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        limit_choices_to={"vocabulary__slug": "gender"},
        related_name="gender_persons",
    )
    gender.verbose_name = _("Gender")

    type = models.ForeignKey(
        Term,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        limit_choices_to={"vocabulary__slug": "naturaltype"},
    )
    type.verbose_name = _("Person Type")

    def age(self):
        if not self.date_of_birth:
            return None
        today = datetime.date.today()
        birth = self.date_of_birth
        return (
            today.year
            - birth.year
            - ((today.month, today.day) < (birth.month, birth.day))
        )

    age.verbose_name = _("Age")

    def save(self, *args, **kwargs):
        if self.autogenerate_displayname:
            self.name = self.first_name + " " + self.last_name
        self.default_sorting_name = self.last_name
        if self.decease_date:
            self.deceased = True
        self._type = (
            self.type
            or global_preferences_registry.manager()["persons__default_naturaltype"]
        )
        self._maintype = "naturalperson"
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
        limit_choices_to={"vocabulary__slug": "legaltype"},
    )
    type.verbose_name = _("Type")

    def save(self, *args, **kwargs):
        self._maintype = "legalperson"
        self._type = (
            self.type
            or global_preferences_registry.manager()["persons__default_legaltype"]
        )
        super().save(*args, **kwargs)

    class Meta:
        ordering = ["name"]
        verbose_name = _("Legal Person")
        verbose_name_plural = _("Legal Persons")


class PersonAssociation(Person):
    type = models.ForeignKey(
        Term,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        limit_choices_to={"vocabulary__slug": "associationtype"},
    )
    type.verbose_name = _("Type")

    def save(self, *args, **kwargs):
        self._maintype = "personassociation"
        self._type = (
            self.type
            or global_preferences_registry.manager()["persons__default_associationtype"]
        )
        super().save(*args, **kwargs)

    class Meta:
        ordering = ["name"]
        verbose_name = _("Person Association")
        verbose_name_plural = _("Person Associations")
