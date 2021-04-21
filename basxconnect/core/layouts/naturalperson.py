import htmlgenerator as hg
from bread import layout
from django.utils.translation import gettext_lazy as _

from basxconnect.core.layouts.person import (
    R,
    C,
    F,
    contact_details,
    relationshipstab,
    style_person,
)


def naturalperson(request):
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
                R(C(hg.H4(_("General")))),
                R(
                    C(
                        R(
                            C(F("salutation")),
                            C(F("title")),
                            C(F("type")),
                        ),
                        R(
                            C(F("first_name")),
                            C(F("last_name")),
                        ),
                        R(
                            C(F("name")),
                            C(F("profession")),
                        ),
                    ),
                    C(
                        R(
                            C(width=1, breakpoint="lg"),
                            C(F("form_of_address")),
                            C(F("gender")),
                            C(width=1, breakpoint="lg"),
                            C(F("preferred_language"), width=4, breakpoint="lg"),
                        ),
                        R(
                            C(width=1, breakpoint="lg"),
                            C(F("salutation_letter")),
                            C(width=1, breakpoint="lg"),
                            C(width=4, breakpoint="lg"),
                        ),
                        R(
                            C(width=1, breakpoint="lg"),
                            C(F("date_of_birth"), width=4, breakpoint="lg"),
                            C(),
                            C(
                                F(
                                    "deceased",
                                    elementattributes={"_class": "standalone"},
                                )
                            ),
                            C(F("decease_date"), width=4, breakpoint="lg"),
                        ),
                    ),
                ),
                gridmode="full-width",
            ),
            hg.DIV(_class="section-separator-bottom"),
            contact_details(request),
        ),
    )
