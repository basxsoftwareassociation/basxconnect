import htmlgenerator as hg
from bread import layout
from bread.utils import reverse
from django.utils.translation import gettext_lazy as _

from basxconnect.core.layouts import editperson
from basxconnect.core.views.person.person_modals_views import (
    NaturalPersonEditMailingsView,
)

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
                    mailings(),
                ),
                contact_details_naturalperson(),
            ),
        ),
    )


def display_field_value(field):
    return R(
        C(
            hg.DIV(
                hg.F(
                    lambda c, e: (c["object"]._meta.get_field(field).verbose_name),
                ),
                style="font-weight: bold;",
            ),
            width=6,
        ),
        C(
            hg.F(
                (
                    lambda c, e: getattr(c["object"], f"get_{field}_display")()
                    if hasattr(c["object"], f"get_{field}_display")
                    else getattr(c["object"], field)
                )
            ),
        ),
        style="padding-bottom: 24px;",
    )


def mailings():
    return tile_with_edit_modal(modal_view=NaturalPersonEditMailingsView)


def tile_with_edit_modal(modal_view):
    modal = layout.modal.Modal.with_ajax_content(
        heading=f"Edit {modal_view.heading()}",
        url=hg.F(
            lambda c, e: reverse(
                modal_view.path(),
                kwargs={"pk": c["object"].pk},
                query={"asajax": True},
            )
        ),
        submitlabel="save",
    )
    displayed_fields = [display_field_value(field) for field in modal_view.fields()]
    return editperson.tiling_col(
        R(C(hg.H4(_(modal_view.heading())))),
        *displayed_fields,
        R(
            C(
                layout.button.Button(
                    "Edit", buttontype="tertiary", icon="edit", **modal.openerattributes
                ),
                modal,
            ),
        ),
        width=8,
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
