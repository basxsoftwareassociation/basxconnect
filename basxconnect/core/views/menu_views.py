from bread import layout as layout
from bread import menu
from bread.utils.links import Link
from bread.utils.urls import reverse, reverse_model
from django.utils.translation import gettext_lazy as _

from .. import models

R = layout.grid.Row
C = layout.grid.Col
F = layout.form.FormField

# MENU ENTRIES ---------------------------------------------------------------------

persongroup = menu.Group(_("Persons"), iconname="group")
settingsgroup = menu.Group(_("Settings"), iconname="settings", order=100)

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
        settingsgroup,
    )
)
menu.registeritem(
    menu.Item(
        Link(
            reverse("basxconnect.core.views.settings_views.personsettings"),
            _("Persons"),
        ),
        settingsgroup,
    )
)
menu.registeritem(
    menu.Item(
        Link(
            reverse("basxconnect.core.views.settings_views.relationshipssettings"),
            _("Relationships"),
        ),
        settingsgroup,
    )
)
