import django.forms
import htmlgenerator as hg
from bread import layout
from bread.layout.components.icon import Icon
from bread.views import AddView, DeleteView, EditView
from django.shortcuts import get_object_or_404
from django.utils.translation import gettext_lazy as _

from basxconnect.core import models


class NaturalPersonEditMailingsView(EditView):
    model = models.NaturalPerson
    fields = [
        "preferred_language",
        "type",
        "salutation_letter",
        "gender",
        "form_of_address",
    ]

    @staticmethod
    def path():
        return "person_modals_views.naturalpersoneditmailingsview"

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
    model = models.NaturalPerson
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
        return "person_modals_views.naturalpersoneditpersonaldataview"

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
    model = models.LegalPerson
    fields = [
        "name",
        "name_addition",
    ]

    @staticmethod
    def path():
        return "person_modals_views.legalpersoneditpersonaldataview"

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
    model = models.PersonAssociation
    fields = [
        "name",
        "preferred_language",
        "salutation_letter",
    ]

    @staticmethod
    def path():
        return "person_modals_views.legalpersoneditpersonaldataview"

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
    model = models.LegalPerson
    fields = [
        "preferred_language",
        "type",
        "salutation_letter",
    ]

    @staticmethod
    def path():
        return "person_modals_views.legalpersoneditmailingsview"

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
    model = models.Postal
    fields = ["type", "address", "postcode", "city", "country"]

    def form_valid(self, form, *args, **kwargs):
        ret = super().form_valid(form, *args, **kwargs)
        is_primary = form.cleaned_data["is_primary"]
        if is_primary:
            self.object.person.primary_postal_address = self.object
        self.object.person.save()
        return ret

    def get_form_class(self, *args, **kwargs):
        class EditPostalForm(super().get_form_class(*args, **kwargs)):
            is_primary = django.forms.BooleanField(
                label=_("Use as primary postal address"), required=False
            )

        return EditPostalForm

    def get_layout(self):
        form_fields = [layout.form.FormField(field) for field in [*self.fields]] + [
            hg.If(
                hg.F(
                    lambda c: c["object"].person.primary_postal_address
                    and c["object"].person.primary_postal_address.pk != c["object"].pk
                ),
                layout.form.FormField("is_primary"),
                "",
            )
        ]
        return hg.DIV(*form_fields)

    @staticmethod
    def path():
        return "person_modals_views.editpostaladdressview"

    @staticmethod
    def edit_heading():
        return _("Edit Postal Address")


class AddPostalAddressView(AddView):
    model = models.Postal

    @staticmethod
    def path():
        return "person_modals_views.addpostaladdressview"

    def post(self, request, *args, **kwargs):
        ret = super().post(request, *args, **kwargs)
        self.object.person.save()
        return ret


class DeletePostalAddressView(DeleteView):
    model = models.Postal

    @staticmethod
    def path():
        return "person_modals_views.deletepostaladdressview"

    def get(self, *args, **kwargs):
        person = get_object_or_404(self.model, pk=self.kwargs.get("pk")).person
        ret = super().get(*args, **kwargs)
        person.save()
        return ret
