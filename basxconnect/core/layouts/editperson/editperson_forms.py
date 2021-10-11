from bread import layout

from basxconnect.core.layouts.editperson import (
    legalperson,
    naturalperson,
    personassociation,
)
from basxconnect.core.layouts.editperson.common import contributions_tab
from basxconnect.core.layouts.editperson.common.relationships_tab import (
    relationshipstab,
)

R = layout.grid.Row
C = layout.grid.Col
F = layout.form.FormField


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

    return [base_data_tab(request), relationshipstab(request), mailing_tab(request)] + (
        [
            contributions_tab.contributions_tab(request),
        ]
        if apps.is_installed("basxconnect.mailer_integration")
        else []
    )
