from bread import layout
from bread.layout.components.icon import Icon
from django.utils.translation import gettext_lazy as _

from basxconnect.core import models
from basxconnect.core.layouts.editperson.common import base_data
from basxconnect.core.layouts.editperson.common.utils import (
    grid_inside_tab,
    person_metadata,
    tile_col_edit_modal,
)

R = layout.grid.Row


def base_data_tab(request):
    return layout.tabs.Tab(
        _("Base data"),
        grid_inside_tab(
            R(
                tile_col_edit_modal(
                    _("Base Data"),
                    models.PersonAssociation,
                    "ajax_edit",
                    Icon("building"),
                    [
                        "name",
                        "preferred_language",
                        "salutation_letter",
                    ],
                ),
                person_metadata(),
            ),
            base_data.common_tiles(request),
        ),
    )
