import htmlgenerator as hg
from basxbread import layout
from basxbread.utils import ModelHref
from django.utils.translation import gettext_lazy as _

R = layout.grid.Row
C = layout.grid.Col


def editperson_toolbar(request):
    deletebutton = layout.button.Button(
        _("Delete"),
        buttontype="ghost",
        icon="trash-can",
        notext=True,
    ).as_submit(
        ModelHref.from_object(hg.C("object"), "delete"),
        confirm_text=hg.format(
            _("Are you sure you want to delete {}?"), hg.EM(hg.C("object"))
        ),
    )
    restorebutton = layout.button.Button(
        _("Restore"),
        buttontype="ghost",
        icon="undo",
        notext=True,
    ).as_submit(
        ModelHref.from_object(hg.C("object"), "delete", query={"restore": True}),
        confirm_text=hg.format(
            _("Are you sure you want to restore {}?"), hg.EM(hg.C("object"))
        ),
    )
    copybutton = layout.button.Button(
        _("Copy"),
        buttontype="ghost",
        icon="copy",
        notext=True,
    ).as_submit(
        ModelHref.from_object(hg.C("object"), "copy"),
        confirm_text=hg.format(
            _("Are you sure you want to copy {}?"), hg.EM(hg.C("object"))
        ),
    )

    return hg.SPAN(
        hg.If(hg.C("object.deleted"), restorebutton, deletebutton),
        copybutton,
        layout.button.PrintPageButton(buttontype="ghost"),
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
