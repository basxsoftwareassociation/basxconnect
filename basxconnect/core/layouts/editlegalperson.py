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
    return editperson.editperson_form(request, base_data_tab)


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
                    editperson.tile_with_edit_modal(LegalPersonEditMailingsView),
                ),
                editperson.contact_details(),
            ),
        ),
    )
