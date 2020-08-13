from bread.admin import BreadAdmin, register
from bread.forms.layout import InlineLayout, Row, Tab, Tabs
from crispy_forms.layout import Div, Fieldset, Layout
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
        Tabs(
            Tab(_("Person"), "name"),
            Tab(
                _("Addresses"),
                Tabs(
                    Tab(
                        "Postal Addresses",
                        InlineLayout(
                            "person_postal_list",
                            Row.with_columns(
                                ("type", 2), ("country", 2), ("address", 8)
                            ),
                        ),
                    ),
                    Tab(
                        "Email Addresses",
                        InlineLayout(
                            "person_email_list",
                            Row.with_columns(("type", 2), ("email", 10)),
                        ),
                    ),
                    Tab(
                        "Phone Numbers",
                        InlineLayout(
                            "person_phone_list",
                            Row.with_columns(("type", 2), ("number", 10)),
                        ),
                    ),
                ),
            ),
        ),
    )


@register
class AddressType(BreadAdmin):
    model = models.AddressType
    browsefields = []


@register
class Relationship(BreadAdmin):
    model = models.Relationship
    editfields = Layout(
        Div(
            Div(
                Fieldset(_("Relationship"), "type", "person_a", "person_b"),
                css_class="col s6",
            ),
            Div(Fieldset(_("Duration"), "start_date", "end_date"), css_class="col s6",),
            css_class="row",
        )
    )


@register
class RelationshipType(BreadAdmin):
    model = models.RelationshipType
    browsefields = []
