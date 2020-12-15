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


def create_term_datatable(title, category_slug):
    return lyt.datatable.DataTable.from_queryset(
        Term.objects.filter(category__slug=category_slug),
        fields=["term"],
        title=title,
        addurl=reverse_model(
            Term,
            "add",
            query={
                "category": Category.objects.get(slug=category_slug).id,
                "next": reverse("basxconnect.core.views.personssettings"),
            },
        ),
        backurl=reverse("basxconnect.core.views.personssettings"),
    )


# a namespacing class to allow the "lazy" definition of layouts
# This is necessary because we will have certain operations, especially
# url reversing, which are only cleanly available after django is completely
# booted up. Layt.init() should be called in one of the AppConfig.ready methods
class Layouts:
    person_edit_layout = None
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

        Layouts.appearancesettings_layout = lyt.BaseElement(lyt.H5(_("Appearance")))

        dist = lyt.DIV(style="margin-bottom: 2rem")
        Layouts.personssettings_layout = lyt.BaseElement(
            lyt.H3(_("Persons")),
            # address type
            create_term_datatable(_("Address types"), "addresstype"),
            dist,
            create_term_datatable(_("Address origins"), "addressorigin"),
            dist,
            create_term_datatable(_("Title"), "title"),
            dist,
            create_term_datatable(
                _("Correspondence Languages"), "correspondence_language"
            ),
            dist,
            create_term_datatable(
                _("Communication Channels"), "communication_channels"
            ),
            dist,
            create_term_datatable(_("Legal Types"), "legaltype"),
            dist,
        )

        Layouts.relationshipssettings_layout = lyt.BaseElement(
            lyt.H3(_("Relationships")),
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

        Layouts.apikeyssettings_layout = lyt.BaseElement(lyt.H3(_("APK Keys")))

        # some shortcuts:
        R = lyt.grid.Row
        C = lyt.grid.Col
        F = lyt.form.FormField

        Layouts.person_edit_layout = lyt.grid.Grid(
            R(C(lyt.H4(_("General Information")))),
            R(
                C(
                    R(
                        C(F("first_name")),
                        C(F("last_name")),
                    ),
                    R(
                        C(F("name")),
                        C(F("preferred_language")),
                    ),
                    R(
                        C(F("date_of_birth")),
                        C(F("profession")),
                    ),
                ),
                C(
                    R(
                        C(F("salutation"), widgetattributes={"width": "18rem"}),
                        C(F("title")),
                    ),
                    R(
                        C(F("salutation")),
                        C(F("salutation_letter")),
                    ),
                ),
            ),
            R(
                C(
                    R(C(lyt.H4(_("Address")))),
                    lyt.form.FormSetField(
                        "core_postal_list",
                        R(C(F("address"))),
                        R(C(F("supplemental_address", widgetattributes={"rows": 1}))),
                        R(
                            C(F("postcode"), breakpoint="lg", width=4),
                            C(F("city"), breakpoint="lg", width=12),
                        ),
                        R(
                            C(F("country")),
                            C(),
                        ),
                        can_delete=False,
                        max_num=1,
                        extra=1,
                    ),
                ),
                C(
                    R(C(lyt.H4(_("Relationships")))),
                    R(C(lyt.H4(_("Communication Channels")))),
                    R(C(lyt.H5(_("Phone")))),
                    lyt.form.FormSetField(
                        "core_phone_list",
                        R(
                            C(F("type"), breakpoint="lg", width=4),
                            C(F("number"), breakpoint="lg", width=12),
                        ),
                        can_delete=False,
                        # max_num=3,
                        extra=0,
                    ),
                    R(C(lyt.H5(_("Email")))),
                    lyt.form.FormSetField(
                        "core_email_list",
                        R(C(F("email"))),
                        can_delete=False,
                        # max_num=3,
                        extra=0,
                    ),
                    # R(C(lyt.H4(_("Notes")))),
                    # lyt.form.FormSetField(
                    # "notes",
                    # R(
                    # C(F("note")),
                    # ),
                    # can_delete=False,
                    # max_num=3,
                    # extra=0,
                    # ),
                ),
            ),
        )
