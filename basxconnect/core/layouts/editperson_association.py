import htmlgenerator as hg
from bread import layout
from django.utils.translation import gettext_lazy as _

from basxconnect.core.layouts.editperson import (
    contact_details,
    relationshipstab,
    style_person,
)

R = layout.grid.Row
C = layout.grid.Col
F = layout.form.FormField


def editperson_association_tabs(request):
    # fix: alignment of tab content and tab should be on global grid I think
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
                R(C(hg.H4(_("General Information")))),
                R(
                    C(
                        R(
                            C(F("name")),
                            C(),
                        ),
                        R(
                            C(),
                            C(F("preferred_language")),
                        ),
                    ),
                    C(
                        R(
                            C(),
                            C(F("salutation_letter")),
                        ),
                    ),
                ),
                gridmode="full-width",
            ),
            hg.DIV(_class="section-separator-bottom"),
            contact_details(request),
        ),
    )
