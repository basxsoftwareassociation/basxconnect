import django.forms
import htmlgenerator as hg
from bread import layout
from bread.layout.components.icon import Icon
from bread.views import AddView, EditView
from django.apps import apps
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
        "autogenerate_displayname",
        "first_name",
        "last_name",
        "date_of_birth",
        "profession",
        "deceased",
        "decease_date",
    ]

    def get_form(self, *args, **kwargs):
        form = super().get_form(*args, **kwargs)
        # only set the disabled attribute on the widget, otherwise we cannot change it on the client side in the future
        if self.object.autogenerate_displayname:
            form.fields["name"].widget.attrs["disabled"] = True
        form.fields["autogenerate_displayname"].widget.attrs[
            "onchange"
        ] = "if(this.checked) { $('input[name=name]').setAttribute('disabled', '') } else { $('input[name=name]').removeAttribute('disabled') }"
        return form

    def get_layout(self):
        R = layout.grid.Row
        C = layout.grid.Col
        F = layout.form.FormField
        return layout.grid.Grid(
            layout.components.forms.Form(
                hg.C("form"),
                R(C(F("salutation"))),
                R(C(F("title"))),
                R(
                    C(
                        F("name"),
                        width=10,
                        breakpoint="lg",
                    ),
                    C(
                        F("autogenerate_displayname"),
                        width=6,
                        breakpoint="lg",
                        style="align-self: flex-end;",
                    ),
                ),
                R(C(F("first_name"))),
                R(C(F("last_name"))),
                R(C(F("date_of_birth"))),
                R(C(F("profession"))),
                R(C(F("deceased"))),
                R(C(F("decease_date"))),
            )
        )


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
    fields = [
        "type",
        "address",
        "postcode",
        "city",
        "country",
        "valid_from",
        "valid_until",
    ]

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
        return hg.DIV(layout.components.forms.Form(hg.C("form"), *form_fields))


class AddPostalAddressView(AddView):
    model = models.Postal

    def form_valid(self, request, *args, **kwargs):
        ret = super().form_valid(request, *args, **kwargs)
        self.object.person.save()
        return ret


class EditEmailAddressView(EditView):
    model = models.Email
    fields = ["type", "email"]

    def form_valid(self, form, *args, **kwargs):

        ret = super().form_valid(form, *args, **kwargs)
        is_primary = form.cleaned_data["is_primary"]
        if is_primary:
            self.object.person.primary_email_address = self.object
        self.object.person.save()

        if apps.is_installed("basxconnect.mailer_integration"):
            from basxconnect.mailer_integration import settings

            new_email = form.cleaned_data["email"]
            propagate_change_to_mailer = (
                form.cleaned_data["propagate_change_to_mailer"]
                and new_email != self.old_email
                and settings.MAILER.email_exists(self.old_email)
                and not settings.MAILER.email_exists(new_email)
            )
            if propagate_change_to_mailer:
                settings.MAILER.change_email_address(self.old_email, new_email)
            elif new_email != self.old_email and hasattr(self.object, "subscription"):
                # if an email-change is not being pushed to the mailer, the subscription is likely to be outdated
                self.object.subscription.delete()
        return ret

    def post(self, request, *args, **kwargs):
        self.old_email = self.get_object().email
        return super().post(request, *args, **kwargs)

    def get_form_class(self, *args, **kwargs):
        class EditEmailForm(super().get_form_class(*args, **kwargs)):
            is_primary = django.forms.BooleanField(
                label=_("Use as primary email address"), required=False
            )
            propagate_change_to_mailer = django.forms.BooleanField(required=False)

            if apps.is_installed("basxconnect.mailer_integration"):
                import basxconnect.mailer_integration.settings as mailer_integration_settings

                propagate_change_to_mailer.label = (
                    _("Propagate change of email address to %s")
                    % mailer_integration_settings.MAILER.name()
                )

        return EditEmailForm

    def get_layout(self):
        form_fields = [layout.form.FormField(field) for field in [*self.fields]] + [
            hg.If(
                hg.F(
                    lambda c: c["object"].person.primary_email_address
                    and c["object"].person.primary_email_address.pk != c["object"].pk
                ),
                layout.form.FormField("is_primary"),
                "",
            ),
            hg.If(
                hg.F(
                    lambda c: apps.is_installed("basxconnect.mailer_integration")
                    and hasattr(c["object"], "subscription")
                ),
                layout.form.FormField("propagate_change_to_mailer"),
                "",
            ),
        ]
        return layout.grid.Grid(
            hg.H3(_("Edit Email")),
            layout.grid.Row(
                layout.grid.Col(
                    layout.form.Form.wrap_with_form(hg.C("form"), hg.DIV(*form_fields)),
                    width=4,
                )
            ),
            gutter=False,
        )


class AddEmailAddressView(AddView):
    model = models.Email

    def post(self, request, *args, **kwargs):
        ret = super().post(request, *args, **kwargs)
        self.object.person.save()
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


class NaturalPersonEditTagsView(EditView):
    model = models.NaturalPerson
    fields = [
        "tags",
    ]


class LegalPersonEditTagsView(EditView):
    model = models.LegalPerson
    fields = [
        "tags",
    ]


class PersonAssociationEditTagsView(EditView):
    model = models.PersonAssociation
    fields = [
        "tags",
    ]
