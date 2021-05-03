import htmlgenerator as hg
from bread import layout
from django.utils.translation import gettext_lazy as _

from basxconnect.core.layouts.editperson import (
    addresses,
    categories,
    email,
    numbers,
    other,
    relationshipstab,
    style_person,
    urls,
)

R = layout.grid.Row
C = layout.grid.Col
F = layout.form.FormField


def editnaturalperson_form(request):
    ret = layout.tabs.Tabs(
        base_data_tab(request),
        relationshipstab(request),
        container=True,
    )
    style_person(ret)
    return ret


def base_data_tab(request):
    return (
        _("Base data"),
        hg.BaseElement(
            layout.grid.Grid(
                R(
                    C(
                        R(C(hg.H4(_("Name")))),
                        R(
                            C(F("salutation"), width=4, breakpoint="lg"),
                            C(F("title"), width=4, breakpoint="lg"),
                        ),
                        R(
                            C(F("first_name")),
                            C(F("last_name")),
                        ),
                        R(
                            C(F("name")),
                        ),
                        _class="section-separator-right",
                    ),
                    C(
                        R(C(hg.H4(_("Mailings")))),
                        R(
                            C(F("preferred_language"), width=4, breakpoint="lg"),
                            C(width=4, breakpoint="lg"),
                            C(F("type"), width=8, breakpoint="lg"),
                        ),
                        R(
                            C(F("salutation_letter"), width=4, breakpoint="lg"),
                            C(F("gender"), width=4, breakpoint="lg"),
                            C(F("form_of_address"), width=8, breakpoint="lg"),
                        ),
                    ),
                ),
                gridmode="full-width",
            ),
            hg.DIV(_class="section-separator-bottom"),
            contact_details_naturalperson(request),
        ),
    )


def contact_details_naturalperson(request):
    return layout.grid.Grid(
        addresses(),
        R(
            numbers(),
            email(),
            _class="section-separator-bottom",
            style="padding-bottom: 2rem",
        ),
        R(
            urls(),
            personal(),
            _class="section-separator-bottom",
            style="padding-bottom: 2rem",
        ),
        R(
            categories(),
            other(),
            style="margin-top: 1rem",
        ),
        gridmode="full-width",
    )


def personal():
    return C(
        hg.H4("Personal"),
        R(C(F("profession"))),
        R(
            C(F("date_of_birth")),
            C(
                F(
                    "deceased",
                    elementattributes={"_class": "standalone"},
                ),
                width=4,
                breakpoint="lg",
            ),
            C(F("decease_date"), width=4, breakpoint="lg"),
        ),
    )
