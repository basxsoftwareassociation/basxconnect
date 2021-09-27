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


class LegalPersonEditPersonalDataView(EditView):
    model = models.LegalPerson
    fields = [
        "name",
        "name_addition",
    ]


class PersonAssociationEditPersonalDataView(EditView):
    model = models.PersonAssociation
    fields = [
        "name",
        "preferred_language",
        "salutation_letter",
    ]


class LegalPersonEditMailingsView(EditView):
    model = models.LegalPerson
    fields = [
        "preferred_language",
        "type",
        "salutation_letter",
    ]


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


class AddPostalAddressView(AddView):
    model = models.Postal

    def post(self, request, *args, **kwargs):
        ret = super().post(request, *args, **kwargs)
        self.object.person.save()
        return ret


class DeletePostalAddressView(DeleteView):
    model = models.Postal

    def get(self, *args, **kwargs):
        person = get_object_or_404(self.model, pk=self.kwargs.get("pk")).person
        ret = super().get(*args, **kwargs)
        person.refresh_from_db()
        person.save()
        return ret


class NaturalPersonEditRemarksView(EditView):
    model = models.NaturalPerson
    fields = [
        "remarks",
    ]


class LegalPersonEditRemarksView(EditView):
    model = models.LegalPerson
    fields = [
        "remarks",
    ]


class PersonAssociationEditRemarksView(EditView):
    model = models.PersonAssociation
    fields = [
        "remarks",
    ]


class NaturalPersonEditCategoriesView(EditView):
    model = models.NaturalPerson
    fields = [
        "categories",
    ]


class LegalPersonEditCategoriesView(EditView):
    model = models.LegalPerson
    fields = [
        "categories",
    ]


class PersonAssociationEditCategoriesView(EditView):
    model = models.PersonAssociation
    fields = [
        "categories",
    ]
