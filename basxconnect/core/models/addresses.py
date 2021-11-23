import htmlgenerator as hg
from bread.layout import button
from django.db import models
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
        limit_choices_to={"vocabulary__slug": "emailtype"},
    )
    type.verbose_name = _("Type")

    def asbutton(self):
        return hg.DIV(
            hg.SPAN(self.email, style="margin-right: 0.25rem"),
            hg.SPAN(style="flex-grow: 1"),
            button.Button(
                icon="email",
                onclick=f"window.location = 'mailto:{self.email}';",
                buttontype="ghost",
                _class="bx--overflow-menu",
            ),
            style="display: flex; flex-wrap: nowrap; align-items: center",
        )

    asbutton.verbose_name = _("Email")

    def __str__(self):
        return str(self.email)

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
        limit_choices_to={"vocabulary__slug": "urltype"},
    )
    type.verbose_name = _("Type")

    def __str__(self):
        return str(self.url)

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
        limit_choices_to={"vocabulary__slug": "phonetype"},
    )
    type.verbose_name = _("Type")

    def __str__(self):
        if self.type:
            return f"{self.number} ({self.type})"
        return str(self.number)

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
        limit_choices_to={"vocabulary__slug": "phonetype"},
    )
    type.verbose_name = _("Type")

    def __str__(self):
        if self.type:
            return f"{self.number} ({self.type})"
        return str(self.number)

    class Meta:
        verbose_name = _("Fax number")
        verbose_name_plural = _("Fax numbers")


class Postal(Address):
    country = CountryField(_("Country"))
    address = models.TextField(_("Address"), blank=True)
    postcode = models.CharField(_("Post Code"), max_length=16, blank=True)
    city = models.CharField(_("City"), max_length=255, blank=True)
    type = models.ForeignKey(
        Term,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="type_%(app_label)s_%(class)s_list",
        limit_choices_to={"vocabulary__slug": "addresstype"},
    )
    type.verbose_name = _("Type")
    valid_from = models.DateField(_("Valid from"), blank=True, null=True)
    valid_until = models.DateField(_("Valid until"), blank=True, null=True)

    def __str__(self):
        ret = [self.address]
        if self.postcode:
            ret.append(f"{self.postcode} {self.city}")
        else:
            ret.append(self.city)
        ret.append(self.country.name)
        return ", ".join(ret)

    class Meta:
        verbose_name = _("Postal address")
        verbose_name_plural = _("Postal addresses")
