from bread import views
from bread.admin import BreadAdmin, BreadGenericAdmin, register
from bread.layout.components import plisplate
from crispy_forms.layout import Div, Fieldset, Layout
from django.utils.translation import gettext_lazy as _

from . import models


@register
class MenuItems(BreadGenericAdmin):
    app_label = "core"

    def menuitems(self):
        return ()


@register
class Person(BreadAdmin):
    model = models.Person
    browse_view = views.BrowseView._with(fields=["name", "preferred_channel"])
    edit_view = views.EditView._with(
        layout=plisplate.DIV(
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

    add_view = views.AddView._with(fields=["name"])

    def menuitems(self):
        return ()


@register
class NaturalPerson(BreadAdmin):
    model = models.NaturalPerson
    # browse_view = views.BrowseView._with(layout=["name", "preferred_channel"])
    edit_view = views.EditView._with(
        layout=plisplate.DIV(
            plisplate.DIV(
                plisplate.grid.Grid(
                    plisplate.grid.Row(
                        plisplate.grid.Col(
                            plisplate.grid.Row(
                                plisplate.FIELDSET(
                                    plisplate.LEGEND(_("Base data")),
                                    plisplate.grid.Grid(
                                        plisplate.grid.Row(
                                            plisplate.grid.Col(
                                                plisplate.form.FormField("first_name")
                                            ),
                                            plisplate.grid.Col(
                                                plisplate.form.FormField("last_name")
                                            ),
                                        ),
                                        plisplate.grid.Row(plisplate.grid.Col("name")),
                                    ),
                                )
                            ),
                            plisplate.grid.Row(
                                plisplate.FIELDSET(
                                    _("Addresses"),
                                    plisplate.grid.Grid(
                                        # TODO Domizil
                                        plisplate.form.FormSetField(
                                            "core_postal_list",
                                            plisplate.grid.Row(
                                                plisplate.grid.Col("Home")
                                            ),
                                            plisplate.grid.Row(
                                                plisplate.grid.Col(
                                                    plisplate.form.FormField("address")
                                                )
                                            ),
                                            plisplate.grid.Row(
                                                plisplate.grid.Col(
                                                    plisplate.form.FormField(
                                                        "postcode"
                                                    ),
                                                ),
                                                plisplate.grid.Col(
                                                    plisplate.form.FormField("city")
                                                ),
                                            ),
                                            plisplate.grid.Row(
                                                plisplate.grid.Col(
                                                    plisplate.form.FormField("country")
                                                )
                                            ),
                                            max_num=1,
                                            extra=1,
                                        ),
                                        # TODO Postfach
                                        plisplate.grid.Row(
                                            plisplate.grid.Col("pobox_name")
                                        ),
                                        plisplate.grid.Row(
                                            plisplate.grid.Col("postcode"),
                                            plisplate.grid.Col("city"),
                                            plisplate.grid.Col("country"),
                                        ),
                                        # TODO Button "more addresses"
                                        # TODO Mailing-Sperre
                                        # TODO Adressherkunft
                                    ),
                                )
                            ),
                        ),
                        plisplate.grid.Col(
                            plisplate.grid.Row(
                                plisplate.FIELDSET(
                                    _("Personal data"),
                                    plisplate.grid.Grid(
                                        plisplate.grid.Row(
                                            plisplate.grid.Col("salutation"),
                                            plisplate.grid.Col("title"),
                                            plisplate.grid.Col("preferred_language"),
                                        ),
                                        # TODO Anrede formal, Briefanrede
                                        plisplate.grid.Row(
                                            plisplate.grid.Col("date_of_birth"),
                                            plisplate.grid.Col("salutation_letter"),
                                        ),
                                    ),
                                )
                            ),
                            # TODO Verknüpfung
                            # TODO Kommunikationskanäle
                        ),
                    ),
                    plisplate.grid.Row(
                        plisplate.grid.Col(
                            plisplate.grid.Row(
                                plisplate.FIELDSET(
                                    _("Categories"),
                                    plisplate.grid.Grid(
                                        # TODO Suche
                                        # TODO Kategorien Labels
                                    ),
                                ),
                            )
                        ),
                        plisplate.grid.Col(
                            # TODO Bemerkungen
                        ),
                    ),
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

    add_view = views.AddView._with(
        layout=plisplate.BaseElement(
            plisplate.form.FormField("first_name"),
            plisplate.form.FormField("last_name"),
        )
    )

    def menuitems(self):
        return ()


@register
class Term(BreadAdmin):
    model = models.Term

    def menuitems(self):
        return ()


@register
class Category(BreadAdmin):
    model = models.Category

    def menuitems(self):
        return ()


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

    def menuitems(self):
        return ()


@register
class RelationshipType(BreadAdmin):
    model = models.RelationshipType

    def menuitems(self):
        return ()
