from bread.admin import BreadAdmin, register
from bread.forms import layout
from crispy_forms.layout import Layout
from django.utils.translation import gettext as _

from . import models


@register
class Person(BreadAdmin):
    model = models.Person
    browsefields = [
        "name",
        "preferred_channel",
    ]
    editfields = Layout(
        layout.Tabs(
            layout.Tab(_("Person"), "name"),
            layout.Tab(
                _("Addresses"), *models.Address.get_contact_related_fieldnames()
            ),
        ),
    )


@register
class AddressType(BreadAdmin):
    model = models.AddressType
    browsefields = ["id"]


@register
class Relationship(BreadAdmin):
    model = models.Relationship


@register
class RelationshipType(BreadAdmin):
    model = models.RelationshipType
    browsefields = []
