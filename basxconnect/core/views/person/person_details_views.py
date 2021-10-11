import logging

import bread
import django
import htmlgenerator as hg
from bread import layout as layout
from bread import menu
from bread.layout.components.form import Form
from bread.utils import reverse_model
from bread.views import EditView, ReadView, layoutasreadonly
from django.apps import apps
from django.conf import settings
from django.forms import forms
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.utils.module_loading import import_string
from django.utils.translation import gettext_lazy as _
from django.views.decorators.csrf import csrf_exempt

from basxconnect.core.layouts.editperson.editperson_forms import (
    editlegalperson_form,
    editnaturalperson_form,
    editpersonassociation_form,
)

from ... import models
from ...layouts.editperson.common.head import editperson_head

R = layout.grid.Row
C = layout.grid.Col
F = layout.form.FormField


def personform_shortcut(request, formlayout):
    return hg.BaseElement(
        layout.grid.Grid(
            editperson_head(request),
            layout.form.Form(hg.C("form"), formlayout),
            gutter=False,
        )
    )


class NaturalPersonEditView(EditView):
    def get_layout(self):
        return personform_shortcut(
            self.request,
            editnaturalperson_form(self.request),
        )


class NaturalPersonReadView(ReadView):
    def get_layout(self):
        return personform_shortcut(
            self.request,
            editnaturalperson_form(self.request),
        )


class LegalPersonEditView(EditView):
    def get_layout(self):
        return personform_shortcut(
            self.request,
            editlegalperson_form(self.request),
        )


class LegalPersonReadView(ReadView):
    def get_layout(self):
        return layoutasreadonly(
            personform_shortcut(
                self.request,
                editlegalperson_form(self.request),
            )
        )


class PersonAssociationEditView(EditView):
    def get_layout(self):
        return personform_shortcut(
            self.request,
            editpersonassociation_form(self.request),
        )


class PersonAssociationReadView(ReadView):
    def get_layout(self):
        return personform_shortcut(
            self.request,
            editpersonassociation_form(self.request),
        )


@csrf_exempt
def togglepersonstatus(request, pk: int):
    if request.method == "POST":
        person = get_object_or_404(models.Person, pk=pk)
        person.active = not person.active
        person.save()
    return HttpResponse(
        _("%s is %s") % (person, _("Active") if person.active else _("Inactive"))
    )


def confirm_delete_email(request, pk: int):
    class ConfirmDeleteEmailForm(forms.Form):
        delete_mailer_contact = django.forms.BooleanField(
            label=_("Delete linked mailer contact as well"),
            required=False,
        )

    email = models.Email.objects.get(id=pk)
    enable_delete_mailer_contact_checkbox = apps.is_installed(
        "basxconnect.mailer_integration"
    ) and hasattr(email, "mailingpreferences")

    if request.method == "POST":
        form = ConfirmDeleteEmailForm(request.POST)
        if form.is_valid():
            person = email.person
            if enable_delete_mailer_contact_checkbox and form.cleaned_data.get(
                "delete_mailer_contact"
            ):
                try:
                    import basxconnect.mailer_integration.settings

                    basxconnect.mailer_integration.settings.MAILER.delete_person(
                        email.email
                    )
                except Exception:
                    logging.error("tried to delete person from mailchimp but failed")

            email.delete()
            person.refresh_from_db()
            person.save()
            return HttpResponseRedirect(
                reverse_model(person, "read", kwargs={"pk": person.pk})
            )
    else:
        form = ConfirmDeleteEmailForm()

    return layout.render(
        request,
        import_string(settings.DEFAULT_PAGE_LAYOUT)(
            menu.main,
            Form.wrap_with_form(
                form,
                hg.BaseElement(
                    hg.H3(_("Delete email %s") % email.email),
                    hg.If(
                        enable_delete_mailer_contact_checkbox,
                        bread.layout.form.FormField("delete_mailer_contact"),
                        hg.BaseElement(),
                    ),
                ),
                submit_label=_("Confirm"),
            ),
        ),
    )
