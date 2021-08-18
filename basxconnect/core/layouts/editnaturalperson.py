import htmlgenerator as hg
from bread import layout
from django.utils.translation import gettext_lazy as _

from basxconnect.core.layouts import editperson
from basxconnect.core.views.person.person_modals_views import (
    NaturalPersonEditMailingsView,
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
                editperson.tiling_col(
                    R(C(hg.H4(_("Name")))),
                    R(
                        C(F("salutation"), width=4),
                        C(F("title"), width=4),
                    ),
                    R(
                        C(F("first_name")),
                        C(F("last_name")),
                    ),
                    R(
                        C(F("name")),
                    ),
                    width=8,
                ),
                editperson.categories(),
            ),
            contact_details_naturalperson(),
        ),
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
                editperson.tile_col_with_edit_modal(
                    modal_view=NaturalPersonEditMailingsView
                ),
                mailer_tile,
            ),
        ),
    )


def contact_details_naturalperson():
    return hg.BaseElement(
        editperson.addresses(),
        R(
            editperson.numbers(),
            editperson.email(),
        ),
        R(
            editperson.urls(),
            personal(),
        ),
        R(editperson.other(), editperson.tiling_col()),
    )


def personal():
    return editperson.tiling_col(
        hg.H4(_("Personal")),
        R(C(F("profession"))),
        R(
            C(F("date_of_birth"), width=6),
            C("", width=1),
            C(
                F(
                    "deceased",
                    elementattributes={"_class": "standalone"},
                ),
                width=3,
            ),
            C(F("decease_date"), width=6),
        ),
    )
