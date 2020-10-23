from bread import views
from bread.admin import BreadAdmin, register
from crispy_forms.layout import Div, Fieldset, Layout
from django.utils.translation import gettext as _

from . import models


@register
class Person(BreadAdmin):
    model = models.Person
    browse_view = views.BrowseView._with(fields=["name", "preferred_channel"])
    edit_view = views.EditView._with(
        fields=Layout(
            Div(
                # Name
                Div(
                    Fieldset(_("Name"), "name", "salutation", "salutation_letter", "preferred_language"),
                    css_class="col s6",
                ),
                # Postal Address
                #Div(
                #    Fieldset(_("Address"), "supplemental_address", "address", "postcode", "city", "country"),
                #    css_class="col s6",
                #),
            )
        )
    )

    add_view = views.AddView._with(fields=["name"])


@register
class NaturalPerson(BreadAdmin):
    model = models.NaturalPerson
    browse_view = views.BrowseView._with(fields=["name", "preferred_channel"])
    edit_view = views.EditView._with(
        fields=Layout(
            Div(
                # Name of NaturalPerson
                Div(
                    Fieldset(_("Name"), "name",
                        "title",
                        "first_name", "middle_name", "last_name", "salutation", "salutation_letter", "preferred_language"),
                    css_class="col s6",
                ),
                # Other attributes of NaturalPerson
                Div(
                    Fieldset(_("Person Details"),
                        # TODO "gender",
                        "date_of_birth", "profession"),
                    css_class="col s6",
                ),
                # Postal Address
                #Div(
                #    Fieldset(_("Address"), "supplemental_address", "address", "postcode", "city", "country"),
                #    css_class="col s6",
                #),
            )
        )
    )

    add_view = views.AddView._with(fields=["name"])


@register
class Term(BreadAdmin):
    model = models.Term


@register
class Category(BreadAdmin):
    model = models.Category


@register
class Relationship(BreadAdmin):
    model = models.Relationship
    browse_view = views.BrowseView._with(fields=["person_a", "type", "person_b"])
    edit_view = views.EditView._with(
        fields=Layout(
            Div(
                Div(
                    Fieldset(_("Relationship"), "person_a", "type", "person_b"),
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
