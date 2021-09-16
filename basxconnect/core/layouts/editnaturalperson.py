import htmlgenerator as hg
from bread import layout
from bread.layout import ObjectFieldValue
from bread.layout.components.icon import Icon
from django.utils.translation import gettext_lazy as _

from basxconnect.core import models
from basxconnect.core.layouts import editperson
from basxconnect.core.layouts.editperson import person_metadata

R = layout.grid.Row
C = layout.grid.Col
F = layout.form.FormField


def editnaturalperson_form(request):
    return editperson.editperson_form(request, base_data_tab, mailings_tab)


def base_data_tab(request):

    return layout.tabs.Tab(
        _("Base data"),
        editperson.grid_inside_tab(
            R(
                personal_data(),
                person_metadata(models.NaturalPerson),
            ),
            contact_details_naturalperson(request),
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
    return editperson.tile_col_edit_modal_displayed_fields(
        _("Personal Data"),
        models.NaturalPerson,
        "ajax_edit_personal_data",
        Icon("user--profile"),
        displayed_fields,
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
                    _("Settings"),
                    models.NaturalPerson,
                    "ajax_edit_mailings",
                    Icon("settings--adjust"),
                    [
                        "preferred_language",
                        "type",
                        "salutation_letter",
                        "gender",
                        "form_of_address",
                    ],
                ),
                mailer_tile,
            ),
        ),
    )


def contact_details_naturalperson(request):
    return hg.BaseElement(
        R(
            editperson.addresses(),
            editperson.numbers(request),
        ),
        R(
            editperson.email(request),
            editperson.urls(request),
        ),
        R(
            editperson.categories(),
            editperson.other(),
        ),
    )
