import htmlgenerator as hg
from basxbread import layout
from basxbread.layout import ObjectFieldLabel, ObjectFieldValue
from basxbread.layout.components.icon import Icon
from basxbread.layout.components.tag import Tag
from django.utils.translation import gettext_lazy as _

from basxconnect.core.layouts.editperson.common import addresses, utils
from basxconnect.core.layouts.editperson.common.utils import (
    open_modal_popup_button,
    tile_with_icon,
)

R = layout.grid.Row


def common_tiles(request):
    return hg.BaseElement(
        R(
            tags(),
            addresses.email(request),
        ),
        R(
            addresses.postals(),
            addresses.numbers(request),
        ),
        R(
            other(),
            addresses.urls(request),
        ),
    )


def other():
    return utils.tile_with_icon(
        Icon("add-comment"),
        hg.H4(_("Other")),
        hg.DIV(
            ObjectFieldLabel("remarks"), style="font-weight:bold; margin-bottom: 1rem;"
        ),
        ObjectFieldValue("remarks"),
        utils.open_modal_popup_button(
            "Remarks",
            hg.C("object").person_ptr,
            "ajax_edit_remarks",
        ),
    )


def tags():
    return tile_with_icon(
        Icon("tag--group"),
        hg.H4(_("Tags")),
        hg.Iterator(hg.F(lambda c: c["object"].tags.all()), "i", Tag(hg.C("i"))),
        open_modal_popup_button(
            _("Edit Tags"),
            hg.C("object").person_ptr,
            "ajax_edit_tags",
        ),
    )
