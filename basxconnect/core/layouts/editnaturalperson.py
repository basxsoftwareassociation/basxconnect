import htmlgenerator as hg
from bread import layout
from django.utils.translation import gettext_lazy as _

from basxconnect.core.layouts import editperson

R = layout.grid.Row
C = layout.grid.Col
F = layout.form.FormField


def editnaturalperson_form(request):
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
                    editperson.tiling_col(
                        R(C(hg.H4(_("Mailings")))),
                        R(
                            C(F("preferred_language"), width=4),
                            C(width=4),
                            C(F("type"), width=8),
                        ),
                        R(
                            C(F("salutation_letter"), width=4),
                            C(F("gender"), width=4),
                            C(F("form_of_address"), width=8),
                        ),
                        width=8,
                    ),
                ),
                contact_details_naturalperson(),
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
        R(editperson.categories(), editperson.other()),
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
