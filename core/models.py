import datetime

from bread.forms.fields import GenericForeignKeyField
from django.contrib.auth import get_user_model
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.utils.html import format_html, linebreaks, mark_safe
from django.utils.translation import gettext as _
from django_countries.fields import CountryField
from languages.fields import LanguageField
from phonenumber_field.modelfields import PhoneNumberField


class Category(models.Model):
    name = models.CharField(_("Name"), max_length=255)
    slug = models.SlugField(
        _("Slug"),
        unique=True,
        help_text=_("slug is human-readable, to make the referencing easier"),
    )

    def __str__(self):
        return self.name

    class Meta:
        ordering = ["name"]


class Term(models.Model):
    category = models.ForeignKey(Category, null=False, on_delete=models.CASCADE)
    category.verbose_name = _("Category")
    term = models.CharField(_("Term"), max_length=255)

    def __str__(self):
        return self.term

    class Meta:
        ordering = ["term"]


class Person(models.Model):
    def preferred_address_choices(field, request, instance):
        if instance is None:
            return []
        objects = []
        for fieldname in Address.get_contact_related_fieldnames():
            objects.extend(getattr(instance, fieldname).all())
        return GenericForeignKeyField.objects_to_choices(objects, required=False)

    name = models.CharField(_("Name"), max_length=255)

    abbreviation_key = models.CharField(
        _("Abbreviation"),
        max_length=255,
        blank=True,
        help_text=_("abbreviation of the name, for quick search of persons"),
    )
    legacy_key = models.CharField(_("Legacy Key"), max_length=255, blank=True)
    # id is the internal key, connect_key is the key that might be used communicated to the person
    connect_key = models.CharField(
        _("Connect Key"),
        max_length=255,
        blank=True,
        help_text=_("This key can be communicated publically"),
    )

    status = models.ForeignKey(
        Term,
        on_delete=models.SET_NULL,
        null=True,
        related_name="personstatus",
        limit_choices_to={"category__slug": "personstatus"},
        help_text=_("eg. active, died, inactive"),
    )
    status.verbose_name = _("Status")

    salutation = models.CharField(
        _("Salutation"), max_length=255, null=True, help_text=_("eg. Frau, Firma")
    )
    salutation_letter = models.CharField(
        _("Salutation Letter"),
        max_length=255,
        null=True,
        help_text=_(
            "eg. Liebe Angela, Sehr geehrte Frau Graber, Liebe Freunde, Sehr geehrte Damen und Herren,"
        ),
    )
    preferred_language = LanguageField(max_length=8, null=True)

    content_type = models.ForeignKey(
        ContentType, on_delete=models.CASCADE, blank=True, null=True
    )
    object_id = models.PositiveIntegerField(blank=True, null=True)
    preferred_address = GenericForeignKey("content_type", "object_id")
    preferred_address.lazy_choices = preferred_address_choices
    preferred_address.verbose_name = _("Preferred address")

    def __str__(self):
        return self.name

    class Meta:
        ordering = ["name"]


class NaturalPerson(Person):
    first_name = models.CharField(_("First Name"), max_length=255)
    middle_name = models.CharField(_("Middle Name"), max_length=255)
    last_name = models.CharField(_("Last Name"), max_length=255)
    title = models.ForeignKey(
        Term,
        on_delete=models.SET_NULL,
        null=True,
        related_name="title",
        limit_choices_to={"category__slug": "title"},
        help_text=_("eg. Herr, Frau, Frau Dr."),
    )
    title.verbose_name = _("Title")
    # TODO: is that something specific for the customer? does this need to be in core?
    profession = models.CharField(
        _("profession"), max_length=255, help_text=_("e.g. nurse, carpenter")
    )
    date_of_birth = models.DateField(_("Date of Birth"), null=True)
    gender = models.ForeignKey(
        Term,
        on_delete=models.SET_NULL,
        null=True,
        related_name="gender",
        limit_choices_to={"category__slug": "gender"},
        help_text=_("eg. male, female, unknown"),
    )
    gender.verbose_name = _("Gender")


# eg. household or family
class GroupPerson(Person):
    class Meta:
        verbose_name = _("Group")
        verbose_name_plural = _("Groups")


class LegalPerson(Person):
    type = models.ForeignKey(
        Term,
        on_delete=models.SET_NULL,
        null=True,
        related_name="legaltype",
        limit_choices_to={"category__slug": "legaltype"},
        help_text=_("eg. Church, Business, Association"),
    )
    type.verbose_name = _("Type")


class Address(models.Model):
    person = models.ForeignKey(
        Person, on_delete=models.CASCADE, related_name="%(app_label)s_%(class)s_list",
    )
    person.verbose_name = _("Person")
    type = models.ForeignKey(
        Term,
        on_delete=models.SET_NULL,
        null=True,
        related_name="%(app_label)s_%(class)s_type",
        limit_choices_to={"category__slug": "addresstype"},
        help_text=_("eg. private, business"),
    )
    type.verbose_name = _("Type")

    status = models.ForeignKey(
        Term,
        on_delete=models.SET_NULL,
        null=True,
        related_name="%(app_label)s_%(class)s_status",
        limit_choices_to={"category__slug": "addressstatus"},
        help_text=_("eg. active, moved, inactive"),
    )
    status.verbose_name = _("Status")

    def send_message(self, subject, message):
        """Should be implemented by subclasses in order send a message to this address"""
        raise NotImplementedError()

    @classmethod
    def get_contact_related_fieldnames(cls):
        for subclass in cls.__subclasses__():
            yield f"{subclass._meta.app_label}_{subclass._meta.model_name}_list"

    class Meta:
        abstract = True


class Email(Address):
    email = models.EmailField(_("Email"))

    def __str__(self):
        return format_html('<a href="mailto:{}">{}</a>', self.email, self.email)

    class Meta:
        verbose_name = _("Email address")
        verbose_name_plural = _("Email addresses")


class PhoneType(models.Model):
    name = models.CharField(
        _("Name for phone type"),
        max_length=255,
        help_text=_("eg. landline, mobile, fax, direct dial"),
    )

    def __str__(self):
        return self.name

    class Meta:
        ordering = ["name"]
        verbose_name = _("Phone type")
        verbose_name_plural = _("Phone types")


class Phone(Address):
    number = PhoneNumberField(_("Number"))
    type = models.ForeignKey(PhoneType, null=True, on_delete=models.SET_NULL)
    type.verbose_name = _("Type")

    def __str__(self):
        return mark_safe(f'<a href="tel:{self.number}">{self.number}</a>')

    class Meta:
        verbose_name = _("Phone number")
        verbose_name_plural = _("Phone numbers")


class County(models.Model):
    name = models.CharField(_("Name of county or state"), max_length=255)
    abbreviation = models.CharField(_("Abbreviation"), max_length=10)
    country = CountryField(_("Country"))


class Postal(Address):
    country = CountryField(_("Country"))
    address = models.TextField(_("Address"))
    supplemental_address = models.TextField(_("Supplemental Address"), blank=True)
    postcode = models.TextField(_("Post Code"), blank=True)
    city = models.TextField(_("City"), blank=True)
    county = models.ForeignKey(County, null=True, on_delete=models.SET_NULL)

    def __str__(self):
        return mark_safe(linebreaks(self.address))

    class Meta:
        verbose_name = _("Postal address")
        verbose_name_plural = _("Postal addresses")


class POBox(Address):
    country = CountryField(_("Country"))
    county = models.ForeignKey(County, null=True, on_delete=models.SET_NULL)
    pobox_name = models.TextField(_("POBox Name"), blank=True)
    pobox_postcode = models.TextField(_("POBox Post Code"), blank=True)
    pobox_city = models.TextField(_("POBox City"), blank=True)

    def __str__(self):
        return mark_safe(linebreaks(self.address))

    class Meta:
        verbose_name = _("Post office box")
        verbose_name_plural = _("Post office boxes")


class RelationshipType(models.Model):
    name = models.CharField(_("Name for relationship type"), max_length=255)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ["name"]
        verbose_name = _("Relationship type")
        verbose_name_plural = _("Relationship types")


class Relationship(models.Model):
    type = models.ForeignKey(RelationshipType, null=True, on_delete=models.SET_NULL)
    type.verbose_name = _("Type")
    person_a = models.ForeignKey(
        Person, on_delete=models.CASCADE, related_name="relationships_to"
    )
    person_a.verbose_name = _("Person A")
    person_b = models.ForeignKey(
        Person, on_delete=models.CASCADE, related_name="relationships_from",
    )
    person_b.verbose_name = _("Person B")
    start_date = models.DateField(_("Starts on"), blank=True, null=True)
    end_date = models.DateField(_("Ends on"), blank=True, null=True)


class Note(models.Model):
    note = models.TextField()
    user = models.ForeignKey(
        get_user_model(), on_delete=models.SET_NULL, null=True, editable=False
    )
    created = models.DateTimeField(auto_now=True)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey("content_type", "object_id")

    def __str__(self):
        ret = f"{self.note}<br/><small><i>{(self.created or datetime.datetime.now() ).date()}"
        if self.user:
            ret += f" - {self.user}"
        ret += "</i></small>"
        return mark_safe(ret)

    class Meta:
        ordering = ["-created"]
