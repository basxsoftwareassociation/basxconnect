﻿import django.forms
import htmlgenerator as hg
from bread import layout
from bread.layout.components.icon import Icon
from bread.utils import reverse_model
from bread.views import AddView, EditView
from django.utils.translation import gettext_lazy as _


class NaturalPersonEditMailingsView(EditView):
    fields = [
        "preferred_language",
        "type",
        "salutation_letter",
        "gender",
        "form_of_address",
    ]

    @staticmethod
    def path():
        return "basxconnect.core.views.person.person_modals_views.naturalpersoneditmailingsview"

    @staticmethod
    def read_heading():
        return _("Settings")

    @staticmethod
    def edit_heading():
        return _("Edit mailing settings")

    @staticmethod
    def icon():
        return Icon("settings--adjust")

    def get_layout(self):
        form_fields = [layout.form.FormField(field) for field in self.fields]
        return hg.DIV(*form_fields)


class NaturalPersonEditPersonalDataView(EditView):
    fields = [
        "salutation",
        "title",
        "name",
        "first_name",
        "last_name",
        "date_of_birth",
        "profession",
        "deceased",
        "decease_date",
    ]

    @staticmethod
    def path():
        return "basxconnect.core.views.person.person_modals_views.naturalpersoneditpersonaldataview"

    @staticmethod
    def read_heading():
        return _("Personal Data")

    @staticmethod
    def edit_heading():
        return _("Edit Personal Data")

    @staticmethod
    def icon():
        return Icon("user--profile")

    def get_layout(self):
        form_fields = [layout.form.FormField(field) for field in self.fields]
        return hg.DIV(*form_fields)


class LegalPersonEditPersonalDataView(EditView):
    fields = [
        "name",
        "name_addition",
    ]

    @staticmethod
    def path():
        return "basxconnect.core.views.person.person_modals_views.legalpersoneditpersonaldataview"

    @staticmethod
    def read_heading():
        return _("Name")

    @staticmethod
    def edit_heading():
        return _("Edit Name")

    @staticmethod
    def icon():
        return Icon("building")

    def get_layout(self):
        form_fields = [layout.form.FormField(field) for field in self.fields]
        return hg.DIV(*form_fields)


class PersonAssociationEditPersonalDataView(EditView):
    fields = [
        "name",
        "preferred_language",
        "salutation_letter",
    ]

    @staticmethod
    def path():
        return "basxconnect.core.views.person.person_modals_views.legalpersoneditpersonaldataview"

    @staticmethod
    def read_heading():
        return _("General Information")

    @staticmethod
    def edit_heading():
        return _("Edit General Information")

    @staticmethod
    def icon():
        return Icon("building")

    def get_layout(self):
        form_fields = [layout.form.FormField(field) for field in self.fields]
        return hg.DIV(*form_fields)


class LegalPersonEditMailingsView(EditView):
    fields = [
        "preferred_language",
        "type",
        "salutation_letter",
    ]

    @staticmethod
    def path():
        return "basxconnect.core.views.person.person_modals_views.legalpersoneditmailingsview"

    @staticmethod
    def read_heading():
        return _("Settings")

    @staticmethod
    def edit_heading():
        return _("Edit mailing settings")

    @staticmethod
    def icon():
        return Icon("settings--adjust")

    def get_layout(self):
        form_fields = [layout.form.FormField(field) for field in self.fields]
        return hg.DIV(*form_fields)


class EditPostalAddressView(EditView):
    fields = ["type", "address", "postcode", "city", "country"]

    def get_success_url(self):
        return reverse_model(
            self.object.person, "read", kwargs={"pk": self.object.person.pk}
        )

    def get_form(self, form_class=None):
        ret = super().get_form(form_class)
        ret.fields["is_primary"] = django.forms.BooleanField(
            label=_("Use as primary postal address"), required=False
        )
        return ret

    def post(self, request, *args, **kwargs):
        ret = super().post(request, *args, **kwargs)
        is_primary = request.POST.get("is_primary")
        if is_primary == "on":
            self.object.person.primary_postal_address = self.object
            self.object.person.save()
        return ret

    def get_layout(self):
        form_fields = [layout.form.FormField(field) for field in [*self.fields]] + [
            hg.If(
                hg.F(
                    lambda c: c["object"].person.primary_postal_address.pk
                    != c["object"].pk
                ),
                layout.form.FormField("is_primary"),
                "",
            )
        ]
        return hg.DIV(*form_fields)

    @staticmethod
    def path():
        return "basxconnect.core.views.person.person_modals_views.editpostaladdressview"

    @staticmethod
    def edit_heading():
        return _("Edit Postal Address")


class AddPostalAddressView(AddView):
    def get_success_url(self):
        return reverse_model(
            self.object.person, "read", kwargs={"pk": self.object.person.pk}
        )

    @staticmethod
    def path():
        return "basxconnect.core.views.person.person_modals_views.addpostaladdressview"
