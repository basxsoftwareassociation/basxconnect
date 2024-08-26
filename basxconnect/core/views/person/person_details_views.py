import logging

import basxbread
import django
import htmlgenerator as hg
from basxbread import layout, menu
from basxbread.layout.components.button import Button
from basxbread.layout.components.forms import Form
from basxbread.utils import Link, reverse_model
from basxbread.views import EditView, ReadView
from django.apps import apps
from django.forms import forms
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.utils.translation import gettext_lazy as _
from django.views.decorators.csrf import csrf_exempt

from ... import models
from ...layouts.editperson import legalperson, naturalperson, personassociation
from ...layouts.editperson.common import history_tab
from ...layouts.editperson.common.head import editperson_head

# from ...layouts.editperson.common.relationships_tab import relationshipstab

R = layout.grid.Row
C = layout.grid.Col


class NaturalPersonEditView(EditView):
    def get_layout(self):
        return personform_shortcut(
            editnaturalperson_form(self.request),
        )


class NaturalPersonReadView(ReadView):
    def get_layout(self):
        return personform_shortcut(
            editnaturalperson_form(self.request),
        )


class LegalPersonEditView(EditView):
    def get_layout(self):
        return personform_shortcut(editlegalperson_form(self.request))


class LegalPersonReadView(ReadView):
    def get_layout(self):
        return personform_shortcut(editlegalperson_form(self.request))


class PersonAssociationEditView(EditView):
    def get_layout(self):
        return personform_shortcut(editpersonassociation_form(self.request))


class PersonAssociationReadView(ReadView):
    def get_layout(self):
        return personform_shortcut(editpersonassociation_form(self.request))


def personform_shortcut(formlayout):
    return hg.BaseElement(
        layout.grid.Grid(
            editperson_head(),
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
    ret = [
        base_data_tab(),
        # relationshipstab(request),
        # mailing_tab(request),
    ]

    if apps.is_installed("basxconnect.contributions"):
        from ...layouts.editperson.common import contributions_tab

        ret.append(contributions_tab.contributions_tab(request))
    if apps.is_installed("basxbread.contrib.publicurls"):
        from ...layouts.editperson.common import documenttemplates_tab

        ret.append(documenttemplates_tab.documenttemplates_tab())
    ret.append(history_tab.history_tab())
    return ret


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
    email = models.Email.objects.get(id=pk)
    enable_delete_mailer_contact_checkbox = apps.is_installed(
        "basxconnect.mailer_integration"
    ) and hasattr(email, "subscription")

    fields = []
    if enable_delete_mailer_contact_checkbox:
        from basxconnect.mailer_integration.settings import MAILER

        class DeleteMailerSubscriptionForm(forms.Form):
            delete_mailer_contact = django.forms.BooleanField(
                label=_("Delete linked %s subscription as well") % MAILER.name(),
                required=False,
            )

        fields.append("delete_mailer_contact")

        if request.method == "POST":
            form = DeleteMailerSubscriptionForm(request.POST)
            if form.is_valid():
                person = email.person
                if enable_delete_mailer_contact_checkbox and form.cleaned_data.get(
                    "delete_mailer_contact"
                ):
                    try:
                        from basxconnect.mailer_integration.settings import MAILER

                        MAILER.delete_person(email.email)
                    except Exception:
                        logging.error("tried to delete person from mailer but failed")

                email.delete()
                person.refresh_from_db()
                person.save()
                return HttpResponseRedirect(
                    reverse_model(person, "read", kwargs={"pk": person.pk})
                )
        else:
            form = DeleteMailerSubscriptionForm()
    else:
        if request.method == "POST":
            form = forms.Form(request.POST)
            if form.is_valid():
                email.delete()
                return HttpResponseRedirect(
                    reverse_model(email.person, "read", kwargs={"pk": email.person.pk})
                )
        else:
            form = forms.Form()

    return layout.render(
        request,
        layout.skeleton.default_page_layout(
            menu.main,
            Form(
                form,
                hg.BaseElement(
                    hg.H3(_("Delete email %s") % email.email),
                    *(basxbread.layout.forms.FormField(field) for field in fields),
                ),
                hg.DIV(
                    Button.from_link(
                        Link(
                            href=reverse_model(
                                email.person, "read", kwargs={"pk": email.person.pk}
                            ),
                            label=_("Cancel"),
                            iconname=None,
                        ),
                        buttontype="tertiary",
                    ),
                    hg.DIV(style="width: 1rem"),
                    *layout.forms.helpers.Submit(_("Confirm")),
                    style="display: flex; ",
                ),
            ),
        ),
    )
