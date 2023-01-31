from basxbread import layout as layout
from basxbread import menu
from basxbread.layout import DEVMODE_KEY
from basxbread.utils.links import Link
from basxbread.utils.urls import reverse, reverse_model
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
        Link(
            reverse_model(models.Person, "browse"),
            _("Persons"),
            iconname="group",
            permissions=[
                f"{models.Person._meta.app_label}.view_{models.Person._meta.model_name}"
            ],
        ),
        persongroup,
    )
)

menu.registeritem(
    menu.Item(
        Link(
            reverse_model(models.Vocabulary, "browse"),
            _("Taxonomy"),
            permissions=[
                f"{models.Vocabulary._meta.app_label}.view_{models.Vocabulary._meta.model_name}"
            ],
        ),
        menu.settingsgroup,
    )
)

menu.registeritem(
    menu.Item(
        Link(
            reverse("basxconnect.core.views.settings_views.relationshipssettings"),
            _("Relationships"),
            permissions=[
                f"{models.RelationshipType._meta.app_label}.view_{models.RelationshipType._meta.model_name}"
            ],
        ),
        menu.settingsgroup,
    )
)
