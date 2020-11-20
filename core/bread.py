from django.utils.translation import gettext_lazy as _

from bread import layout as plisplate
from bread import menu, views
from bread.admin import BreadAdmin, BreadGenericAdmin, register

from . import models
from .wizards.add_person import AddPersonWizard


@register
class MenuItems(BreadGenericAdmin):
    app_label = "core"

    def menuitems(self):
        settingsgroup = menu.Group(_("Settings"), icon="settings")
        persongroup = menu.Group(_("Persons"), icon="group")
        return [
            menu.Item(menu.Link(Person().reverse("browse"), _("Persons")), persongroup),
            menu.Item(menu.Link("/", _("General")), settingsgroup),
            menu.Item(menu.Link("/", _("Appearance")), settingsgroup),
            menu.Item(menu.Link("/", _("Persons")), settingsgroup),
            menu.Item(menu.Link("/", _("Relationships")), settingsgroup),
            menu.Item(menu.Link("/", _("API Keys")), settingsgroup),
        ]


@register
class Person(BreadAdmin):
    model = models.Person
    add_view = AddPersonWizard

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
    filterset_fields = ["category__slug"]

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
        layout=plisplate.DIV(
            plisplate.DIV(
                plisplate.FIELDSET(_("Relationship"), "person_a", "type", "person_b"),
                css_class="col s6",
            ),
            plisplate.DIV(
                plisplate.FIELDSET(_("Duration"), "start_date", "end_date"),
                css_class="col s6",
            ),
            css_class="row",
        )
    )
    add_view = views.AddView._with(layout=edit_view.layout)

    def menuitems(self):
        return ()


@register
class RelationshipType(BreadAdmin):
    model = models.RelationshipType

    def menuitems(self):
        return ()
