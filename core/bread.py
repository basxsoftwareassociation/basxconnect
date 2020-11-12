from bread import views
from bread.admin import BreadAdmin, register
from crispy_forms.layout import Div, Fieldset, Layout
from django.utils.translation import gettext as _

from bread.layout import (
    DIV,
    HTML,
    FieldLabel,
    FieldValue,
    InlineLayout,
    Grid,
    Row,
    Col,
)

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
                    Fieldset(
                        _("Name"),
                        "name",
                        "salutation",
                        "salutation_letter",
                        "preferred_language",
                    ),
                    css_class="col s6",
                ),
                # Postal Address
                # Div(
                #    Fieldset(_("Address"), "supplemental_address", "address", "postcode", "city", "country"),
                #    css_class="col s6",
                # ),
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
                Grid(
                    Row(
                        Col(
                            Row(
                                Fieldset(
                                    # TODO translation
                                    _("Stammdaten"),
                                    Grid(
                                        Row(Col("first_name"), Col("last_name")),
                                        Row(Col("name")),
                                    )
                                )
                            ),
                            Row(
                                Fieldset(
                                    # TODO translation
                                    _("Adressen"),
                                    Grid(
                                        # TODO Domizil
                                        Row(Col("address")),
                                        Row(Col("postcode"), Col("city"), Col("country")),
                                        # TODO Postfach
                                        Row(Col("pobox_name")),
                                        Row(Col("postcode"), Col("city"), Col("country")),
                                        # TODO Button "more addresses"
                                        # TODO Mailing-Sperre
                                        # TODO Adressherkunft
                                    )
                                )
                            ),
                        ),

                        Col(
                            Row(
                                Fieldset(
                                    # TODO translation
                                    _("Personendaten"),
                                    Grid(
                                        Row(Col("salutation"), Col("title"), Col("preferred_language")),
                                        # TODO Anrede formal, Briefanrede
                                        Row(Col("date_of_birth"), Col("salutation_letter")),
                                    )
                                )
                            ),
                            # TODO Verknüpfung
                            # TODO Kommunikationskanäle
                        ),
                    ),
                    Row(
                        Col(
                            Row(
                                Fieldset(
                                    # TODO translation
                                    _("Kategorien"),
                                    Grid(
                                        # TODO Suche
                                        # TODO Kategorien Labels
                                        )
                                    ),
                                )
                        ),
                        Col(
                            # TODO Bemerkungen
                            )
                        )
                ),
            )
        )
      )

#                Div(
#                    Fieldset(
#                        _("Name"),
#                        Grid(
#                            Row(
#                                Col("name"), Col("title")
#                            ),  # without breakpoint and width: even distribution of columns
#                            Row(Col("first_name"), Col("last_name")),
#                            Row(  # use breakpoint and width to change the number of "units" used for one cell
##                                Col("salutation", breakpoint="lg", width=3),
#                                Col("salutation_letter", breakpoint="lg", width=4),
#                            ),
#                        #"middle_name",
#                        #"preferred_language",
#                        ),
#                    ),
#                ),
#                # Other attributes of NaturalPerson
#                Div(
#                    Fieldset(
#                        _("Person Details"), "gender", "date_of_birth", "profession"
#                    ),
#                    css_class="col s6",
#                ),
#                # Postal Address
#                Div(
#                    InlineLayout(
#                        "core_postal_list",
#                        Div(
#                            Fieldset(_("Address"), "supplemental_address", "address", "postcode", "city", "country"),
#                        ),
#                        formset_kwargs={"extra": 1, "max_num": 1},
#                    ),
#                ),
#            )
#        )
#    )

    add_view = views.AddView._with(fields=["first_name", "last_name"])


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
