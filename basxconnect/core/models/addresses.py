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
        blank=True,
        related_name="type_%(app_label)s_%(class)s_list",
        limit_choices_to={"category__slug": "addresstype"},
    )
    type.verbose_name = _("Type")

    status = models.ForeignKey(
        Term,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="status_%(app_label)s_%(class)s_list",
        limit_choices_to={"category__slug": "addressstatus"},
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
    type = models.ForeignKey(
        Term,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="type_%(app_label)s_%(class)s_list",
        limit_choices_to={"category__slug": "addresstype"},
    )

    def __str__(self):
        return format_html('<a href="mailto:{}">{}</a>', self.email, self.email)

    class Meta:
        verbose_name = _("Email address")
        verbose_name_plural = _("Email addresses")


class Web(Address):
    url = models.URLField(_("Url"))
    type = models.ForeignKey(
        Term,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="type_%(app_label)s_%(class)s_list",
        limit_choices_to={"category__slug": "urltype"},
    )

    def __str__(self):
        return format_html('<a href="{}">{}</a>', self.url, self.url)

    class Meta:
        verbose_name = _("Web address")
        verbose_name_plural = _("Web addresses")


class Phone(Address):
    number = PhoneNumberField(_("Number"))
    type = models.ForeignKey(
        Term,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        limit_choices_to={"category__slug": "phonetype"},
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
        blank=True,
        limit_choices_to={"category__slug": "phonetype"},
    )
    type.verbose_name = _("Type")

    def __str__(self):
        if self.type:
            return f"{self.number} ({self.type})"
        return self.number

    class Meta:
        verbose_name = _("Fax number")
        verbose_name_plural = _("Fax numbers")


class Postal(Address):
    country = CountryField(_("Country"))
    address = models.TextField(
        _("Address"), blank=True, help_text="Street, house, PO box"
    )
    postcode = models.CharField(_("Post Code"), max_length=16, blank=True)
    city = models.CharField(_("City"), max_length=255, blank=True)

    def __str__(self):
        ret = [self.address]
        if self.postcode:
            ret.append(f"{self.postcode} {self.city}")
        else:
            ret.append(self.city)
        ret.append(self.country.name)
        return linebreaksbr("\n".join(ret))

    class Meta:
        verbose_name = _("Postal address")
        verbose_name_plural = _("Postal addresses")
