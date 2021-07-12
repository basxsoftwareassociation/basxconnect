import htmlgenerator as hg
from bread import layout
from bread.utils import reverse
from django.utils.translation import gettext_lazy as _

from basxconnect.core.layouts import editperson

R = layout.grid.Row
C = layout.grid.Col
F = layout.form.FormField


def editnaturalperson_form(request):
    return editperson.editperson_form(request, base_data_tab)


def base_data_tab():
    modal = layout.modal.Modal.with_ajax_content(
        heading="hello world",
        url=hg.F(
            lambda c, e: reverse(
                "basxconnect.core.views.person.person_details_views.naturalpersoneditnameview",
                kwargs={"pk": c["object"].pk},
                query={"asajax": True},
            )
        ),
        submitlabel="save",
    )

    return layout.tabs.Tab(
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
                        R(
                            C(
                                layout.button.Button(
                                    "Edit",
                                    **modal.openerattributes,
                                    style="float: right"
                                ),
                                modal,
                            ),
                        ),
                        width=7,
                        breakpoint="lg",
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
                        _class="bx--offset-xlg-1",
                        width=7,
                        breakpoint="lg",
                    ),
                ),
                gridmode="full-width",
                gutter=False,
            ),
            contact_details_naturalperson(),
        ),
    )


def contact_details_naturalperson():
    return layout.grid.Grid(
        editperson.addresses(),
        R(
            editperson.numbers(),
            editperson.email(),
        ),
        R(
            editperson.urls(),
            personal(),
        ),
        R(
            editperson.categories(),
            editperson.other(),
        ),
        gridmode="full-width",
        gutter=False,
    )


def personal():
    return C(
        hg.H4(_("Personal")),
        R(C(F("profession"))),
        R(
            C(F("date_of_birth"), width=6, breakpoint="lg"),
            C("", width=1, breakpoint="lg"),
            C(
                F(
                    "deceased",
                    elementattributes={"_class": "standalone"},
                ),
                width=3,
                breakpoint="lg",
            ),
            C(F("decease_date"), width=6, breakpoint="lg"),
        ),
    )
