from bread import layout as layout
from bread import menu
from bread.utils.urls import reverse, reverse_model
from django.utils.translation import gettext_lazy as _

from .. import models

R = layout.grid.Row
C = layout.grid.Col
F = layout.form.FormField

# MENU ENTRIES ---------------------------------------------------------------------

persongroup = menu.Group(_("Persons"), icon="group")
settingsgroup = menu.Group(_("Settings"), icon="settings", order=100)

menu.registeritem(
    menu.Item(
        menu.Link(reverse_model(models.Person, "browse"), _("Persons")), persongroup
    )
)

menu.registeritem(
    menu.Item(
        menu.Link(reverse("basxconnect.core.views.generalsettings"), _("General")),
        settingsgroup,
    )
)
menu.registeritem(
    menu.Item(
        menu.Link(reverse("basxconnect.core.views.personsettings"), _("Persons")),
        settingsgroup,
    )
)
menu.registeritem(
    menu.Item(
        menu.Link(
            reverse("basxconnect.core.views.relationshipssettings"),
            _("Relationships"),
        ),
        settingsgroup,
    )
)
