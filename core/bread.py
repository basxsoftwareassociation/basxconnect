from bread import views
from bread.admin import BreadAdmin, register
from crispy_forms.layout import Div, Fieldset, Layout
from django.utils.translation import gettext as _

from . import models


@register
class Person(BreadAdmin):
    model = models.Person
    browse_view = views.BrowseView._with(fields=["name", "preferred_channel"])
    edit_view = views.EditView._with(fields=["name", "person_postal_list"])


@register
class Term(BreadAdmin):
    model = models.Term


@register
class Category(BreadAdmin):
    model = models.Category


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
