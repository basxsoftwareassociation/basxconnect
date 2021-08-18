import htmlgenerator as hg
from bread import layout
from django.utils.translation import gettext_lazy as _

from basxconnect.core.layouts import editperson
from basxconnect.core.views.person.person_modals_views import (
    LegalPersonEditMailingsView,
)

R = layout.grid.Row
C = layout.grid.Col
F = layout.form.FormField


def editlegalperson_form(request):
    return editperson.editperson_form(request, base_data_tab, mailings_tab)


def base_data_tab():
    return layout.tabs.Tab(
        _("Base data"),
        hg.BaseElement(
            editperson.grid_inside_tab(
                R(
                    editperson.tiling_col(
                        R(C(hg.H4(_("Name")))),
                        R(
                            C(
                                R(C(F("name"))),
                                R(C(F("name_addition"))),
                                width=8,
                            )
                        ),
                    ),
                    editperson.categories(),
                ),
                editperson.contact_details(),
            ),
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
                    modal_view=LegalPersonEditMailingsView
                ),
                mailer_tile,
            ),
        ),
    )
