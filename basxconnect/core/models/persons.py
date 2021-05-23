from bread import layout
from bread.utils import get_concrete_instance, pretty_modelname
from django.contrib.contenttypes.fields import GenericRelation
from django.db import models
from django.utils.translation import gettext_lazy as _
from languages.fields import LanguageField
from simple_history.models import HistoricalRecords

from .. import settings
from .utils import Note, Term

LanguageField.db_collation = None  # fix issue with LanguageField in django 3.2


class PersonManager(models.Manager):
    def get_queryset(self, *args, **kwargs):
        return super().get_queryset(*args, **kwargs).filter(deleted=False)

    def get_deleted(self, *args, **kwargs):
        return super().get_queryset(*args, **kwargs).filter(deleted=True)


class Person(models.Model):
    deleted = models.BooleanField(_("Deleted"), blank=True, default=False)
    personnumber = models.CharField(
        _("Person number"), max_length=255, unique=True, blank=True
    )
    personnumber.sorting_name = "personnumber__int"
    name = models.CharField(_("Display name"), max_length=255, blank=True)
    active = models.BooleanField(_("Active"), default=True)
    salutation_letter = models.CharField(
        _("Salutation Letter"),
        max_length=255,
        blank=True,
    )
    preferred_language = LanguageField(
        _("Preferred Language"), blank=True, max_length=8
    )  # mitigate up-stream bug
    preferred_language.lazy_choices = (
        lambda field, request, instance: settings.PREFERRED_LANGUAGES
    )

    categories = models.ManyToManyField(
        Term, blank=True, limit_choices_to={"category__slug": "category"}
    )
    categories.verbose_name = _("Categories")

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
    _type.verbose_name = _("Category")

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
        created = self.pk
        # automatically generate a person number if empty
        # if this object is just beeing create we do not have
        # a person number (because there is no pk) and we need
        # to do the same thing again after a call to super.save
        # and then save again
        if not self.personnumber:
            self.personnumber = str(self.pk or "")

        if not self._maintype:
            self._maintype = "person"
        if hasattr(self, "core_postal_list"):
            if (
                self.core_postal_list.all().count() == 1
                or self.primary_postal_address is None
            ):
                self.primary_postal_address = self.core_postal_list.first()
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
        if not self.personnumber:
            self.personnumber = str(self.pk)
            super().save(*args, **kwargs)

        # this signal needs to be sent manually in order to trigger the search-index update
        # Django does only send a signal for the child-model but our search-index only observes
        # this base model
        models.signals.post_save.send(
            sender=Person,
            instance=self,
            created=created,
            update_fields=kwargs.get("update_fields"),
            raw=False,
            using=kwargs.get("using"),
        )

    def search_index_snippet(self):
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
    title = models.ForeignKey(
        Term,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        limit_choices_to={"category__slug": "title"},
        related_name="title_persons",
    )
    title.verbose_name = _("Title")
    salutation = models.ForeignKey(
        Term,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        limit_choices_to={"category__slug": "salutation"},
        related_name="+",
    )
    salutation.verbose_name = _("Salutation")

    form_of_address = models.ForeignKey(
        Term,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        limit_choices_to={"category__slug": "form_of_address"},
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
        limit_choices_to={"category__slug": "gender"},
        related_name="gender_persons",
    )
    gender.verbose_name = _("Gender")

    type = models.ForeignKey(
        Term,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        limit_choices_to={"category__slug": "naturaltype"},
    )
    type.verbose_name = _("Person category")

    def save(self, *args, **kwargs):
        if not self.name:
            self.name = self.first_name + " " + self.last_name
        if self.decease_date:
            self.deceased = True
        self._type = self.type
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
        limit_choices_to={"category__slug": "legaltype"},
    )
    type.verbose_name = _("Type")

    def save(self, *args, **kwargs):
        self._maintype = "legalperson"
        self._type = self.type
        super().save(*args, **kwargs)

    class Meta:
        ordering = ["name"]
        verbose_name = _("Legal Person")
        verbose_name_plural = _("Legal Persons")


LegalPerson._meta.get_field("name").verbose_name = _("Name")


class PersonAssociation(Person):
    type = models.ForeignKey(
        Term,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        limit_choices_to={"category__slug": "associationtype"},
    )
    type.verbose_name = _("Type")

    def save(self, *args, **kwargs):
        self._maintype = "personassociation"
        self._type = self.type
        super().save(*args, **kwargs)

    class Meta:
        ordering = ["name"]
        verbose_name = _("Person Association")
        verbose_name_plural = _("Person Associations")
