from basxbread import layout as layout
from basxbread import menu, utils
from basxbread.layout import DEVMODE_KEY
from django.utils.translation import gettext_lazy as _

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

persongroup = menu.Group(_("Persons"), iconname="group")

menu.registeritem(
    menu.Item(
        utils.Link(
            utils.reverse_model(models.Person, "browse"),
            _("Persons"),
            iconname="group",
            permissions=[utils.permissionname(models.Person, "view")],
        ),
        persongroup,
    )
)

menu.registeritem(
    menu.Item(
        utils.Link(
            utils.reverse_model(models.Vocabulary, "browse"),
            _("Taxonomy"),
            permissions=[utils.permissionname(models.Vocabulary, "view")],
        ),
        menu.settingsgroup,
    )
)

menu.registeritem(
    menu.Item(
        utils.Link(
            utils.reverse(
                "basxconnect.core.views.settings_views.relationshipssettings"
            ),
            _("Relationships"),
            permissions=[utils.permissionname(models.RelationshipType, "view")],
        ),
        menu.settingsgroup,
    )
)
