import logging

import bread
import django
import htmlgenerator as hg
from bread import layout, menu
from bread.layout.components.button import Button
from bread.layout.components.forms import Form
from bread.utils import Link, reverse_model
from bread.views import EditView, ReadView, layoutasreadonly
from django.apps import apps
from django.conf import settings
from django.forms import forms
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.utils.module_loading import import_string
from django.utils.translation import gettext_lazy as _
from django.views.decorators.csrf import csrf_exempt

from ... import models
from ...layouts.editperson import legalperson, naturalperson, personassociation
from ...layouts.editperson.common.head import editperson_head
from ...layouts.editperson.common.relationships_tab import relationshipstab

R = layout.grid.Row
C = layout.grid.Col


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


def personform_shortcut(request, formlayout):
    return hg.BaseElement(
        layout.grid.Grid(
            editperson_head(request),
            formlayout,
            gutter=False,
        )
    )


def editnaturalperson_form(request):
    return editperson_form(
        request,
        naturalperson.base_data_tab,
        naturalperson.mailings_tab,
    )


def editpersonassociation_form(request):
    return editperson_form(
        request,
        personassociation.base_data_tab,
        personassociation.mailings_tab,
    )


def editlegalperson_form(request):
    return editperson_form(
        request,
        legalperson.base_data_tab,
        legalperson.mailings_tab,
    )


def editperson_form(request, base_data_tab, mailings_tab):
    return R(
        C(
            layout.grid.Grid(
                layout.tabs.Tabs(
                    *editperson_tabs(base_data_tab, mailings_tab, request),
                    tabpanel_attributes={
                        "_class": "tile-container",
                        "style": "padding: 0;",
                    },
                    labelcontainer_attributes={
                        "_class": "tabs-lg",
                        "style": "background-color: white;",
                    },
                ),
                gutter=False,
            ),
        ),
    )


def editperson_tabs(base_data_tab, mailing_tab, request):

    from django.apps import apps

    if apps.is_installed("basxconnect.contributions"):
        from ...layouts.editperson.common import contributions_tab

        return [
            base_data_tab(request),
            relationshipstab(request),
            mailing_tab(request),
            contributions_tab.contributions_tab(request),
        ]
    return [
        base_data_tab(request),
        relationshipstab(request),
        mailing_tab(request),
    ]


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
            label=_("Delete linked email subscriptions as well"),
            required=False,
        )

    email = models.Email.objects.get(id=pk)
    enable_delete_mailer_contact_checkbox = apps.is_installed(
        "basxconnect.mailer_integration"
    ) and hasattr(email, "subscription")

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
            hg.FORM(
                Form(
                    form,
                    hg.BaseElement(
                        hg.H3(_("Delete email %s") % email.email),
                        hg.If(
                            enable_delete_mailer_contact_checkbox,
                            bread.layout.form.FormField("delete_mailer_contact"),
                            hg.BaseElement(),
                        ),
                    ),
                    standalone=False,
                ),
                hg.DIV(
                    Button(_("Save"), type="submit"),
                    _class="bx--form-item",
                    style="margin-top: 2rem; display: inline-block;",
                ),
                hg.DIV(
                    Button.fromlink(
                        Link(
                            href=reverse_model(
                                email.person, "read", kwargs={"pk": email.person.pk}
                            ),
                            label=_("Cancel"),
                            iconname=None,
                        ),
                        buttontype="tertiary",
                    ),
                    _class="bx--form-item",
                    style="margin-top: 2rem; display: inline-block; margin-left: 1rem;",
                ),
            ),
        ),
    )
