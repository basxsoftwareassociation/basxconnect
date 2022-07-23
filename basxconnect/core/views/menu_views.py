from basxbread import layout as layout
from basxbread import menu
from basxbread.layout import DEVMODE_KEY
from basxbread.utils.links import Link
from basxbread.utils.urls import reverse, reverse_model
from django.utils.translation import gettext_lazy as _

import basxconnect.core.models

from .. import models


# New menu group with developer mode checking
class DevGroup(menu.Group):
    def has_permission(self, request):
        return super().has_permission(request) and request.session.get(
            DEVMODE_KEY, False
        )


class SuperUserItem(menu.Item):
    def has_permission(self, request):
        return super().has_permission(request) and request.user.is_superuser


R = layout.grid.Row
C = layout.grid.Col
F = layout.forms.FormField

# MENU ENTRIES ---------------------------------------------------------------------

menu.registeritem(
    menu.Item(
        Link(
            reverse("core.vocabulary.browse"),
            basxconnect.core.models.Vocabulary._meta.verbose_name_plural,
        ),
        menu.admingroup,
    )
)

persongroup = menu.Group(_("Persons"), iconname="group")

menu.registeritem(
    menu.Item(
        Link(reverse_model(models.Person, "browse"), _("Persons"), iconname="group"),
        persongroup,
    )
)

menu.registeritem(
    menu.Item(
        Link(
            reverse("basxconnect.core.views.settings_views.generalsettings"),
            _("General"),
        ),
        menu.settingsgroup,
    )
)

menu.registeritem(
    menu.Item(
        Link(
            reverse("basxconnect.core.views.settings_views.personsettings"),
            _("Persons"),
        ),
        menu.settingsgroup,
    )
)

menu.registeritem(
    menu.Item(
        Link(
            reverse("basxconnect.core.views.settings_views.relationshipssettings"),
            _("Relationships"),
        ),
        menu.settingsgroup,
    )
)
