import htmlgenerator as hg
from bread import layout
from django.utils.translation import gettext_lazy as _

from basxconnect.core.layouts import editperson

R = layout.grid.Row
C = layout.grid.Col
F = layout.form.FormField


def editpersonassociation_form(request):
    return editperson.editperson_form(request, base_data_tab)


def base_data_tab():
    return layout.tabs.Tab(
        _("Base data"),
        hg.BaseElement(
            layout.grid.Grid(
                R(C(hg.H4(_("General Information")))),
                R(
                    C(
                        R(
                            C(F("name"), width=4, breakpoint="lg"),
                            C(F("preferred_language"), width=2, breakpoint="lg"),
                            C(F("salutation_letter"), width=4, breakpoint="lg"),
                        ),
                    ),
                ),
                gutter=False,
            ),
            editperson.contact_details(),
        ),
    )
