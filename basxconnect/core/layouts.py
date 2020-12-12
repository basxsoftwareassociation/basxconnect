from bread import layout as lyt
from bread.utils.urls import reverse, reverse_model
from django.utils.translation import gettext_lazy as _

from .models import Category, RelationshipType, Term


def single_item_fieldset(related_field, fieldname, queryset=None):
    """Helper function to show only a single item of a (foreign-key) related item list"""
    return lyt.form.FormSetField(
        related_field,
        lyt.form.FormField(fieldname),
        formsetinitial={"queryset": queryset},
        can_delete=False,
        max_num=1,
        extra=1,
    )


# a namespacing class to allow the "lazy" definition of layouts
# This is necessary because we will have certain operations, especially
# url reversing, which are only cleanly available after django is completely
# booted up. Layt.init() should be called in one of the AppConfig.ready methods
class Layouts:
    person_edit_layout = None
    person_browse_layout = None
    generalsettings_layout = None
    appearancesettings_layout = None
    personssettings_layout = None
    relationshipssettings_layout = None
    apikeyssettings_layout = None

    @staticmethod
    def init():
        Layouts.generalsettings_layout = lyt.BaseElement(
            lyt.grid.Grid(
                lyt.grid.Row(lyt.grid.Col(lyt.form.FormField("type"))),
                lyt.grid.Row(lyt.grid.Col(lyt.form.FormField("name"))),
                lyt.grid.Row(lyt.grid.Col(lyt.form.FormField("name_addition"))),
            ),
            lyt.form.FormSetField(
                "core_postal_list",
                lyt.grid.Grid(
                    lyt.grid.Row(lyt.grid.Col(lyt.form.FormField("address"))),
                    lyt.grid.Row(
                        lyt.grid.Col(lyt.form.FormField("supplemental_address"))
                    ),
                    lyt.grid.Row(
                        lyt.grid.Col(
                            lyt.form.FormField("postcode"), breakpoint="lg", width=2
                        ),
                        lyt.grid.Col(
                            lyt.form.FormField("city"), breakpoint="lg", width=3
                        ),
                        lyt.grid.Col(
                            lyt.form.FormField("country"), breakpoint="lg", width=3
                        ),
                    ),
                ),
                can_delete=False,
                max_num=1,
                extra=1,
            ),
            lyt.grid.Grid(
                lyt.grid.Row(
                    lyt.grid.Col(single_item_fieldset("core_phone_list", "number")),
                    lyt.grid.Col(single_item_fieldset("core_fax_list", "number")),
                ),
                lyt.grid.Row(
                    lyt.grid.Col(
                        single_item_fieldset(
                            "core_email_list",
                            "email",
                        )
                    ),
                    lyt.grid.Col(single_item_fieldset("core_web_list", "url")),
                ),
            ),
            lyt.form.SubmitButton(_("Save")),
        )

        Layouts.appearancesettings_layout = lyt.BaseElement(lyt.H2(_("Appearance")))

        dist = lyt.DIV(style="margin-bottom: 2rem")
        Layouts.personssettings_layout = lyt.BaseElement(
            lyt.H2(_("Persons")),
            # address type
            lyt.datatable.DataTable.from_queryset(
                Term.objects.filter(category__slug="addresstype"),
                fields=["term"],
                title=_("Address types"),
                addurl=reverse_model(
                    Term,
                    "add",
                    query={
                        "category": Category.objects.get(slug="addresstype").id,
                        "next": reverse("basxconnect.core.views.personssettings"),
                    },
                ),
                backurl=reverse("basxconnect.core.views.personssettings"),
            ),
            dist,
            # address origin
            lyt.datatable.DataTable.from_queryset(
                Term.objects.filter(category__slug="addressorigin"),
                fields=["term"],
                title=_("Address origins"),
                addurl=reverse_model(
                    Term,
                    "add",
                    query={
                        "category": Category.objects.get(slug="addressorigin").id,
                        "next": reverse("basxconnect.core.views.personssettings"),
                    },
                ),
                backurl=reverse("basxconnect.core.views.personssettings"),
            ),
            dist,
            # salutation
            lyt.datatable.DataTable.from_queryset(
                Term.objects.filter(category__slug="salutation"),
                fields=["term"],
                title=_("Salutation"),
                addurl=reverse_model(
                    Term,
                    "add",
                    query={
                        "category": Category.objects.get(slug="salutation").id,
                        "next": reverse("basxconnect.core.views.personssettings"),
                    },
                ),
                backurl=reverse("basxconnect.core.views.personssettings"),
            ),
            dist,
        )

        Layouts.relationshipssettings_layout = lyt.BaseElement(
            lyt.H2(_("Relationships")),
            lyt.datatable.DataTable.from_queryset(
                RelationshipType.objects.all(),
                fields=["name"],
                addurl=reverse_model(
                    RelationshipType,
                    "add",
                    query={
                        "next": reverse("basxconnect.core.views.relationshipssettings")
                    },
                ),
                backurl=reverse("basxconnect.core.views.relationshipssettings"),
            ),
        )

        Layouts.apikeyssettings_layout = lyt.BaseElement(lyt.H2(_("APK Keys")))
        Layouts.person_edit_layout = lyt.DIV(
            lyt.DIV(
                lyt.grid.Grid(
                    lyt.grid.Row(
                        lyt.grid.Col(
                            lyt.grid.Row(
                                lyt.FIELDSET(
                                    lyt.LEGEND(_("Base data")),
                                    lyt.grid.Grid(
                                        lyt.grid.Row(
                                            lyt.grid.Col(
                                                lyt.form.FormField("first_name")
                                            ),
                                            lyt.grid.Col(
                                                lyt.form.FormField("last_name")
                                            ),
                                        ),
                                        lyt.grid.Row(
                                            lyt.grid.Col(lyt.form.FormField("name"))
                                        ),
                                    ),
                                )
                            ),
                            lyt.grid.Row(
                                lyt.FIELDSET(
                                    _("Addresses"),
                                    lyt.grid.Grid(
                                        # Home Address
                                        lyt.form.FormSetField(
                                            "core_postal_list",
                                            lyt.grid.Row(lyt.grid.Col(_("Home"))),
                                            lyt.grid.Row(
                                                lyt.grid.Col(
                                                    lyt.form.FormField("address")
                                                )
                                            ),
                                            lyt.grid.Row(
                                                lyt.grid.Col(
                                                    lyt.form.FormField("postcode"),
                                                ),
                                                lyt.grid.Col(
                                                    lyt.form.FormField("city")
                                                ),
                                            ),
                                            lyt.grid.Row(
                                                lyt.grid.Col(
                                                    lyt.form.FormField("country")
                                                )
                                            ),
                                            max_num=1,
                                            extra=1,
                                        ),
                                        # PO Box
                                        lyt.form.FormSetField(
                                            "core_pobox_list",
                                            lyt.grid.Row(
                                                lyt.grid.Col(_("Post office box"))
                                            ),
                                            lyt.grid.Row(
                                                lyt.grid.Col(
                                                    lyt.form.FormField("pobox_name")
                                                )
                                            ),
                                            lyt.grid.Row(
                                                lyt.grid.Col(
                                                    lyt.form.FormField("postcode")
                                                ),
                                                lyt.grid.Col(
                                                    lyt.form.FormField("city")
                                                ),
                                                lyt.grid.Col(
                                                    lyt.form.FormField("country")
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
                        lyt.grid.Col(
                            lyt.grid.Row(
                                lyt.FIELDSET(
                                    _("Personal data"),
                                    lyt.grid.Grid(
                                        lyt.grid.Row(
                                            lyt.grid.Col(
                                                lyt.form.FormField("salutation")
                                            ),
                                            lyt.grid.Col(lyt.form.FormField("title")),
                                            lyt.grid.Col(
                                                lyt.form.FormField("preferred_language")
                                            ),
                                        ),
                                        # TODO Anrede formal, Briefanrede
                                        lyt.grid.Row(
                                            lyt.grid.Col(
                                                lyt.form.FormField("date_of_birth")
                                            ),
                                            lyt.grid.Col(
                                                lyt.form.FormField("salutation_letter")
                                            ),
                                        ),
                                    ),
                                )
                            ),
                            # TODO Verknüpfung
                            # TODO Kommunikationskanäle
                        ),
                    ),
                    lyt.grid.Row(
                        lyt.grid.Col(
                            lyt.grid.Row(
                                lyt.FIELDSET(
                                    _("Categories"),
                                    lyt.grid.Grid(
                                        # TODO Suche
                                        # TODO Kategorien Labels
                                    ),
                                ),
                            )
                        ),
                        lyt.grid.Col(
                            # TODO Bemerkungen
                        ),
                    ),
                ),
            )
        )
