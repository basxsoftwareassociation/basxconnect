from bread import layout
from bread.layout.components.icon import Icon
from django.utils.translation import gettext_lazy as _

from basxconnect.core import models
from basxconnect.core.layouts.editperson.common.addresses import addresses
from basxconnect.core.layouts.editperson.common.base_data_building_blocks import (
    grid_inside_tab,
    other,
    person_metadata,
    tags,
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
                person_metadata(models.LegalPerson),
            ),
            addresses(request),
            R(
                tags(),
                other(),
            ),
        ),
    )
