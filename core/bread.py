from django.shortcuts import redirect
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from bread import layout as tpl
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
            menu.Item(
                menu.Link(reverse("core.views.generalsettings"), _("General")),
                settingsgroup,
            ),
            # menu.Item(
            # menu.Link(reverse("core.views.appearancesettings"), _("Appearance")),
            # settingsgroup,
            # ),
            menu.Item(
                menu.Link(reverse("core.views.personssettings"), _("Persons")),
                settingsgroup,
            ),
            menu.Item(
                menu.Link(
                    reverse("core.views.relationshipssettings"), _("Relationships")
                ),
                settingsgroup,
            ),
            # menu.Item(
            # menu.Link(reverse("core.views.apikeyssettings"), _("API Keys")),
            # settingsgroup,
            # ),
        ]


@register
class Person(BreadAdmin):
    model = models.Person
    # nr, status, person typ, name, str, plz, place, country
    browse_view = views.BrowseView._with(
        layout=[
            "number",
            "status",
            "type",
            "name",
            "street",
            "postalcode",
            "city",
            "country",
        ]
    )
    add_view = lambda a, b: redirect("core:person:add_wizard", step="Search")  # noqa
    add_wizard_view = AddPersonWizard

    def menuitems(self):
        return ()


@register
class NaturalPerson(BreadAdmin):
    model = models.NaturalPerson
    # browse_view = views.BrowseView._with(layout=["name", "preferred_channel"])
    edit_view = views.EditView._with(
        layout=tpl.DIV(
            tpl.DIV(
                tpl.grid.Grid(
                    tpl.grid.Row(
                        tpl.grid.Col(
                            tpl.grid.Row(
                                tpl.FIELDSET(
                                    tpl.LEGEND(_("Base data")),
                                    tpl.grid.Grid(
                                        tpl.grid.Row(
                                            tpl.grid.Col(
                                                tpl.form.FormField("first_name")
                                            ),
                                            tpl.grid.Col(
                                                tpl.form.FormField("last_name")
                                            ),
                                        ),
                                        tpl.grid.Row(
                                            tpl.grid.Col(tpl.form.FormField("name"))
                                        ),
                                    ),
                                )
                            ),
                            tpl.grid.Row(
                                tpl.FIELDSET(
                                    _("Addresses"),
                                    tpl.grid.Grid(
                                        # Home Address
                                        tpl.form.FormSetField(
                                            "core_postal_list",
                                            tpl.grid.Row(tpl.grid.Col(_("Home"))),
                                            tpl.grid.Row(
                                                tpl.grid.Col(
                                                    tpl.form.FormField("address")
                                                )
                                            ),
                                            tpl.grid.Row(
                                                tpl.grid.Col(
                                                    tpl.form.FormField("postcode"),
                                                ),
                                                tpl.grid.Col(
                                                    tpl.form.FormField("city")
                                                ),
                                            ),
                                            tpl.grid.Row(
                                                tpl.grid.Col(
                                                    tpl.form.FormField("country")
                                                )
                                            ),
                                            max_num=1,
                                            extra=1,
                                        ),
                                        # PO Box
                                        tpl.form.FormSetField(
                                            "core_pobox_list",
                                            tpl.grid.Row(
                                                tpl.grid.Col(_("Post office box"))
                                            ),
                                            tpl.grid.Row(
                                                tpl.grid.Col(
                                                    tpl.form.FormField("pobox_name")
                                                )
                                            ),
                                            tpl.grid.Row(
                                                tpl.grid.Col(
                                                    tpl.form.FormField("postcode")
                                                ),
                                                tpl.grid.Col(
                                                    tpl.form.FormField("city")
                                                ),
                                                tpl.grid.Col(
                                                    tpl.form.FormField("country")
                                                ),
                                            ),
                                            max_num=1,
                                            extra=1,
                                        )
                                        # TODO Button "more addresses"
                                        # TODO Mailing-Sperre
                                        # TODO Adressherkunft
                                    ),
                                )
                            ),
                        ),
                        tpl.grid.Col(
                            tpl.grid.Row(
                                tpl.FIELDSET(
                                    _("Personal data"),
                                    tpl.grid.Grid(
                                        tpl.grid.Row(
                                            tpl.grid.Col(
                                                tpl.form.FormField("salutation")
                                            ),
                                            tpl.grid.Col(tpl.form.FormField("title")),
                                            tpl.grid.Col(
                                                tpl.form.FormField("preferred_language")
                                            ),
                                        ),
                                        # TODO Anrede formal, Briefanrede
                                        tpl.grid.Row(
                                            tpl.grid.Col(
                                                tpl.form.FormField("date_of_birth")
                                            ),
                                            tpl.grid.Col(
                                                tpl.form.FormField("salutation_letter")
                                            ),
                                        ),
                                    ),
                                )
                            ),
                            # TODO Verknüpfung
                            # TODO Kommunikationskanäle
                        ),
                    ),
                    tpl.grid.Row(
                        tpl.grid.Col(
                            tpl.grid.Row(
                                tpl.FIELDSET(
                                    _("Categories"),
                                    tpl.grid.Grid(
                                        # TODO Suche
                                        # TODO Kategorien Labels
                                    ),
                                ),
                            )
                        ),
                        tpl.grid.Col(
                            # TODO Bemerkungen
                        ),
                    ),
                ),
            )
        )
    )

    add_view = views.AddView._with(
        layout=tpl.BaseElement(
            tpl.form.FormField("first_name"),
            tpl.form.FormField("last_name"),
        )
    )

    def menuitems(self):
        return ()


@register
class JuristicPerson(BreadAdmin):
    model = models.JuristicPerson

    def menuitems(self):
        return ()


@register
class PersonAssociation(BreadAdmin):
    model = models.PersonAssociation

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
        layout=tpl.DIV(
            tpl.DIV(
                tpl.FIELDSET(_("Relationship"), "person_a", "type", "person_b"),
                css_class="col s6",
            ),
            tpl.DIV(
                tpl.FIELDSET(_("Duration"), "start_date", "end_date"),
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
