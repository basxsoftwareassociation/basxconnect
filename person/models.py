from bread.forms.fields import GenericForeignKeyField
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.utils.html import format_html, linebreaks, mark_safe
from django.utils.translation import gettext as _
from django_countries.fields import CountryField
from phonenumber_field.modelfields import PhoneNumberField
from birthday.fields import BirthdayField


class Person(models.Model):
    def preferred_address_choices(field, request, instance):
        if instance is None:
            return []
        objects = []
        for fieldname in Address.get_contact_related_fieldnames():
            objects.extend(getattr(instance, fieldname).all())
        return GenericForeignKeyField.objects_to_choices(objects, required=False)

    name = models.CharField(_("Name"), max_length=255)

    # eg. Frau, Firma
    salutation = models.CharField(_("Salutation"), max_length=255, null=True)
    # eg. Liebe Angela, Sehr geehrte Frau Graber, Liebe Freunde, Sehr geehrte Damen und Herren,
    salutation_letter = models.CharField(_("Salutation Letter"), max_length=255, null=True)

    # prefered address
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
        #abstract = True
        ordering = ["name"]


class NaturalPerson(Person):
    first_name = models.CharField(_("First Name"), max_length=255)
    middle_name = models.CharField(_("Middle Name"), max_length=255)
    last_name = models.CharField(_("Last Name"), max_length=255)
    # eg. Dr.
    # TODO: should this be a lookup table instead?
    title = models.CharField(_("Title"), max_length=255)
    # eg. Nurse
    # TODO: is that something specific for the customer? does this need to be in core?
    profession = models.CharField(_("profession"), max_length=255)
    # https://pypi.org/project/django-birthday/
    date_of_birth: BirthdayField()


# eg. household or family
class GroupPerson(Person):

    class Meta:
        verbose_name = _("Group")
        verbose_name_plural = _("Groups")


class LegalType(models.Model):
    # eg. Company, Church, Association
    name = models.CharField(_("Name for legal type"), max_length=255)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ["name"]
        verbose_name = _("Legal type")
        verbose_name_plural = _("Legal types")


class LegalPerson(Person):
    type = models.ForeignKey(LegalType, null=True, on_delete=models.SET_NULL)
    type.verbose_name = _("Type")


class AddressType(models.Model):
    # eg. private, business
    name = models.CharField(_("Name for address type"), max_length=255)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ["name"]
        verbose_name = _("Address type")
        verbose_name_plural = _("Address types")


class Address(models.Model):
    person = models.ForeignKey(
        Person, on_delete=models.CASCADE, related_name="%(app_label)s_%(class)s_list",
    )
    person.verbose_name = _("Person")
    type = models.ForeignKey(AddressType, null=True, on_delete=models.SET_NULL)
    type.verbose_name = _("Type")

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
    # eg. landline, mobile, fax, direct dial
    name = models.CharField(_("Name for phone type"), max_length=255)

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
    supplemental_address = models.TextField(_("Supplemental Address"), default="")
    postcode = models.TextField(_("Post Code"), default="")
    city = models.TextField(_("City"), default="")
    county = models.ForeignKey(County, null=True, on_delete=models.SET_NULL)
    pobox_name = models.TextField(_("POBox Name"), default="")
    pobox_postcode = models.TextField(_("POBox Post Code"), default="")
    pobox_city = models.TextField(_("POBox City"), default="")

    def __str__(self):
        return mark_safe(linebreaks(self.address))

    class Meta:
        verbose_name = _("Postal address")
        verbose_name_plural = _("Postal addresses")


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
