from django.db import models
from django.template.defaultfilters import linebreaksbr
from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _
from django_countries.fields import CountryField
from phonenumber_field.modelfields import PhoneNumberField

from .persons import Person
from .utils import Term


class Address(models.Model):
    person = models.ForeignKey(
        Person,
        on_delete=models.CASCADE,
        related_name="%(app_label)s_%(class)s_list",
    )
    person.verbose_name = _("Person")
    type = models.ForeignKey(
        Term,
        on_delete=models.SET_NULL,
        null=True,
        related_name="type_%(app_label)s_%(class)s_list",
        limit_choices_to={"category__slug": "addresstype"},
        help_text=_("eg. Private, Business"),
    )
    type.verbose_name = _("Type")

    status = models.ForeignKey(
        Term,
        on_delete=models.SET_NULL,
        null=True,
        related_name="status_%(app_label)s_%(class)s_list",
        limit_choices_to={"category__slug": "addressstatus"},
        help_text=_("eg. active, moved, inactive"),
    )
    status.verbose_name = _("Status")

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


class Web(Address):
    url = models.URLField(_("Url"))

    def __str__(self):
        return format_html('<a href="{}">{}</a>', self.url, self.url)

    class Meta:
        verbose_name = _("Web address")
        verbose_name_plural = _("Web addresses")


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
    type = models.ForeignKey(
        Term,
        on_delete=models.SET_NULL,
        null=True,
        limit_choices_to={"category__slug": "phonetype"},
        help_text=_("eg. Private, Business"),
    )
    type.verbose_name = _("Type")

    def __str__(self):
        if self.type:
            return f"{self.number} ({self.type})"
        return self.number

    class Meta:
        verbose_name = _("Phone number")
        verbose_name_plural = _("Phone numbers")


class Fax(Address):
    number = PhoneNumberField(_("Number"))
    type = models.ForeignKey(
        Term,
        on_delete=models.SET_NULL,
        null=True,
        limit_choices_to={"category__slug": "phonetype"},
        help_text=_("eg. Private, Business"),
    )
    type.verbose_name = _("Type")

    def __str__(self):
        if self.type:
            return f"{self.number} ({self.type})"
        return self.number

    class Meta:
        verbose_name = _("Fax number")
        verbose_name_plural = _("Fax numbers")


class County(models.Model):
    name = models.CharField(_("Name of county or state"), max_length=255)
    abbreviation = models.CharField(_("Abbreviation"), max_length=10)
    country = CountryField(_("Country"))


class Postal(Address):
    country = CountryField(_("Country"))
    county = models.ForeignKey(County, null=True, on_delete=models.SET_NULL)
    county.verbose_name = _("County")
    address = models.CharField(
        _("Address"), max_length=255, help_text=_("Street and House Number")
    )
    supplemental_address = models.TextField(_("Supplemental Address"), blank=True)
    postcode = models.CharField(_("Post Code"), max_length=16, blank=True)
    city = models.CharField(_("City"), max_length=255)

    def __str__(self):
        ret = [self.address]
        if self.supplemental_address:
            ret.append(self.supplemental_address)
        if self.postcode:
            ret.append(f"{self.postcode} {self.city}")
        else:
            ret.append(self.city)
        if self.county:
            ret.append(self.county)
        ret.append(self.country.name)
        return linebreaksbr("\n".join(ret))

    class Meta:
        verbose_name = _("Postal address")
        verbose_name_plural = _("Postal addresses")


class POBox(Address):
    country = CountryField(_("Country"))
    county = models.ForeignKey(County, null=True, on_delete=models.SET_NULL)
    county.verbose_name = _("County")
    pobox_name = models.CharField(_("POBox"), max_length=255)
    postcode = models.CharField(_("Post Code"), max_length=16, blank=True)
    city = models.CharField(_("City"), max_length=255)

    def __str__(self):
        ret = [self.pobox_name]
        if self.postcode:
            ret.append(f"{self.postcode} {self.city}")
        else:
            ret.append(self.city)
        if self.county:
            ret.append(self.county)
        ret.append(self.country)
        return linebreaksbr("\n".join(ret))

    class Meta:
        verbose_name = _("Post office box")
        verbose_name_plural = _("Post office boxes")
