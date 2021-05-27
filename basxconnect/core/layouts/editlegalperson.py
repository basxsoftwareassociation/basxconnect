import htmlgenerator as hg
from bread import layout
from django.utils.translation import gettext_lazy as _

from basxconnect.core.layouts import editperson

R = layout.grid.Row
C = layout.grid.Col
F = layout.form.FormField


def editlegalperson_form(request):
    return editperson.editperson_form(request, base_data_tab)


def base_data_tab():
    return layout.tabs.Tab(
        _("Base data"),
        hg.BaseElement(
            layout.grid.Grid(
                R(
                    C(
                        R(C(hg.H4(_("Name")))),
                        R(
                            C(
                                R(C(F("name"))),
                                R(C(F("name_addition"))),
                                width=8,
                                breakpoint="lg",
                            )
                        ),
                    ),
                    C(
                        R(C(hg.H4(_("Mailings")))),
                        R(
                            C(F("preferred_language"), width=4, breakpoint="lg"),
                            C(F("type"), width=8, breakpoint="lg"),
                        ),
                        R(
                            C(F("salutation_letter"), width=12, breakpoint="lg"),
                        ),
                    ),
                ),
                gutter=False,
            ),
            editperson.contact_details(),
        ),
    )
