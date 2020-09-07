from bread.forms.fields import GenericForeignKeyField
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.utils.html import format_html, linebreaks, mark_safe
from django.utils.translation import gettext as _
from django_countries.fields import CountryField
from phonenumber_field.modelfields import PhoneNumberField


class Person(models.Model):
    def preferred_address_choices(field, request, instance):
        if instance is None:
            return []
        objects = []
        for fieldname in Address.get_contact_related_fieldnames():
            objects.extend(getattr(instance, fieldname).all())
        return GenericForeignKeyField.objects_to_choices(objects, required=False)

    name = models.CharField(_("Name"), max_length=255)

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
        ordering = ["name"]


class AddressType(models.Model):
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


class Phone(Address):
    number = PhoneNumberField(_("Number"))

    def __str__(self):
        return mark_safe(f'<a href="tel:{self.number}">{self.number}</a>')

    class Meta:
        verbose_name = _("Phone number")
        verbose_name_plural = _("Phone numbers")


class Postal(Address):
    country = CountryField(_("Country"))
    address = models.TextField(_("Address"))
    postcode = models.TextField(_("Post Code"), default='')
    city = models.TextField(_("City"), default='')

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
