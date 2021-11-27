from bread import layout
from bread.layout.components.icon import Icon
from django.utils.translation import gettext_lazy as _

from basxconnect.core import models
from basxconnect.core.layouts.editperson.common.utils import (
    grid_inside_tab,
    tile_col_edit_modal,
    tiling_col,
)

R = layout.grid.Row
C = layout.grid.Col


def mailings_tab(request):
    from django.apps import apps

    if apps.is_installed("basxconnect.mailer_integration"):
        from basxconnect.mailer_integration.layouts import mailer_integration_tile

        mailer_tile = mailer_integration_tile(request)
    else:
        mailer_tile = tiling_col()

    return layout.tabs.Tab(
        _("Mailings"),
        grid_inside_tab(
            R(
                tile_col_edit_modal(
                    _("Settings"),
                    models.NaturalPerson,
                    "ajax_edit_mailings",
                    Icon("settings--adjust"),
                    [
                        "preferred_language",
                        "type",
                        "salutation_letter",
                        "gender",
                        "form_of_address",
                    ],
                ),
                mailer_tile,
            ),
        ),
    )
