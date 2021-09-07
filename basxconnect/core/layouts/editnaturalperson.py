import htmlgenerator as hg
from bread import layout
from bread.layout import ObjectFieldValue
from django.utils.translation import gettext_lazy as _

from basxconnect.core.layouts import editperson
from basxconnect.core.layouts.editperson import person_metadata
from basxconnect.core.views.person.person_modals_views import (
    NaturalPersonEditMailingsView,
    NaturalPersonEditPersonalDataView,
)

R = layout.grid.Row
C = layout.grid.Col
F = layout.form.FormField


def editnaturalperson_form(request):
    return editperson.editperson_form(request, base_data_tab, mailings_tab)


def base_data_tab():

    return layout.tabs.Tab(
        _("Base data"),
        editperson.grid_inside_tab(
            R(
                personal_data(),
                person_metadata(),
            ),
            contact_details_naturalperson(),
        ),
    )


def personal_data():
    displayed_fields = [
        editperson.display_field_value(field)
        for field in [
            "salutation",
            "title",
            "name",
            "first_name",
            "last_name",
            "date_of_birth",
            "profession",
        ]
    ] + [
        hg.If(ObjectFieldValue("deceased"), editperson.display_field_value("deceased")),
        hg.If(
            ObjectFieldValue("deceased"),
            editperson.display_field_value("decease_date"),
        ),
    ]
    return editperson.tile_col_edit_modal_selected_fields(
        NaturalPersonEditPersonalDataView, displayed_fields
    )


def mailings_tab(request):
    from django.apps import apps

    if apps.is_installed("basxconnect.mailer_integration"):
        from basxconnect.mailer_integration.layouts import mailer_integration_tile

        mailer_tile = mailer_integration_tile(request)
    else:
        mailer_tile = editperson.tiling_col()

    return layout.tabs.Tab(
        _("Mailings"),
        editperson.grid_inside_tab(
            R(
                editperson.tile_col_edit_modal(
                    modal_view=NaturalPersonEditMailingsView
                ),
                mailer_tile,
            ),
        ),
    )


def contact_details_naturalperson():
    return hg.BaseElement(
        R(
            editperson.addresses(),
            editperson.numbers(),
        ),
        R(
            editperson.email(),
            editperson.urls(),
        ),
        R(
            editperson.categories(),
            editperson.other(),
        ),
    )
