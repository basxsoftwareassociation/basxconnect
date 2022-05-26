from bread import layout
from django.utils.translation import gettext_lazy as _

from basxconnect.core.layouts.editperson.common.utils import grid_inside_tab, tiling_col

R = layout.grid.Row


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
                mailer_tile,
                tiling_col(),
            ),
        ),
    )
