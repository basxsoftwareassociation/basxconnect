from bread import views
from bread.admin import BreadAdmin, register
from bread.layout import InlineLayout, Row, Tab, Tabs
from crispy_forms.layout import Div, Fieldset, Layout
from django.utils.translation import gettext as _

from . import models


@register
class Core(BreadAdmin):
    model = models.Person
    browse_view = views.BrowseView._with(fields=["name", "preferred_channel"])
    edit_view = views.EditView._with(
        fields=Layout(
            Tabs(
                Tab(_("Person"), "name"),
                Tab(
                    _("Addresses"),
                    Tabs(
                        Tab(
                            "Postal Addresses",
                            InlineLayout(
                                "core_postal_list",
                                Row.with_columns(
                                    ("type", 2),
                                    ("country", 2),
                                    ("address", 8),
                                    ("postcode", 2),
                                    ("city", 4),
                                ),
                            ),
                        ),
                        Tab(
                            "Email Addresses",
                            InlineLayout(
                                "core_email_list",
                                Row.with_columns(("type", 2), ("email", 10)),
                            ),
                        ),
                        Tab(
                            "Phone Numbers",
                            InlineLayout(
                                "core_phone_list",
                                Row.with_columns(("type", 2), ("number", 10)),
                            ),
                        ),
                    ),
                ),
            ),
        )
    )
    add_view = views.AddView._with(fields=edit_view.fields)


@register
class AddressType(BreadAdmin):
    model = models.AddressType
    browse_view = views.BrowseView._with(fields=[])


@register
class Relationship(BreadAdmin):
    model = models.Relationship
    edit_view = views.EditView._with(
        fields=Layout(
            Div(
                Div(
                    Fieldset(_("Relationship"), "type", "person_a", "person_b"),
                    css_class="col s6",
                ),
                Div(
                    Fieldset(_("Duration"), "start_date", "end_date"),
                    css_class="col s6",
                ),
                css_class="row",
            )
        )
    )
    add_view = views.AddView._with(fields=edit_view.fields)


@register
class RelationshipType(BreadAdmin):
    model = models.RelationshipType
    browse_view = views.BrowseView._with(fields=[])
