import htmlgenerator as hg
from bread import layout
from bread.utils import reverse_model
from django.utils.translation import gettext_lazy as _

from basxconnect.core.models import Person

R = layout.grid.Row
C = layout.grid.Col


def editperson_toolbar(request):
    deletebutton = layout.button.Button(
        _("Delete"),
        buttontype="ghost",
        icon="trash-can",
        notext=True,
        **layout.aslink_attributes(
            hg.F(lambda c: layout.objectaction(c["object"], "delete"))
        ),
    )
    restorebutton = layout.button.Button(
        _("Restore"),
        buttontype="ghost",
        icon="undo",
        notext=True,
        **layout.aslink_attributes(
            hg.F(
                lambda c: layout.objectaction(
                    c["object"], "delete", query={"restore": True}
                )
            )
        ),
    )
    copybutton = layout.button.Button(
        _("Copy"),
        buttontype="ghost",
        icon="copy",
        notext=True,
        **layout.aslink_attributes(
            hg.F(lambda c: layout.objectaction(c["object"], "copy"))
        ),
    )

    add_person_button = layout.button.Button(
        _("Add person"),
        buttontype="primary",
        icon="add",
        notext=True,
        **layout.aslink_attributes(hg.F(lambda c: reverse_model(Person, "add"))),
    )
    return hg.SPAN(
        hg.If(hg.C("object.deleted"), restorebutton, deletebutton),
        copybutton,
        layout.button.PrintPageButton(buttontype="ghost"),
        add_person_button,
        _class="no-print",
        style="margin-bottom: 1rem; margin-left: 1rem",
        width=3,
    )


def editperson_head(request):
    return hg.BaseElement(
        R(
            C(
                hg.H3(
                    hg.SPAN(
                        hg.C("object"),
                        style=hg.If(
                            hg.C("object.deleted"), "text-decoration: line-through"
                        ),
                    ),
                    editperson_toolbar(request),
                ),
                width=12,
            ),
            style="padding-top: 1rem",
        ),
    )
