from bread import layout as layout
from bread.layout import register as registerlayout
from bread.utils.urls import reverse, reverse_model
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _

from .models import Category, RelationshipType, Term

R = layout.grid.Row
C = layout.grid.Col
F = layout.form.FormField


@registerlayout()
def editperson_head():
    active_toggle = layout.toggle.Toggle(None, _("Inactive"), _("Active"))
    active_toggle.input.attributes["id"] = "person_active_toggle"
    active_toggle.input.attributes["hx_trigger"] = "change"
    active_toggle.input.attributes["hx_post"] = layout.F(
        lambda c, e: reverse_lazy("core.person.togglestatus", args=[c["object"].pk])
    )
    active_toggle.input.attributes["checked"] = layout.F(
        lambda c, e: c["object"].active
    )
    active_toggle.label.insert(0, _("Person status"))
    active_toggle.label.attributes["_for"] = active_toggle.input.attributes["id"]

    personnumber = layout.DIV(
        layout.LABEL(layout.ModelFieldLabel("personnumber"), _class="bx--label"),
        layout.DIV(layout.ModelFieldValue("personnumber"), style="margin-top: 1rem"),
    )
    persontype = layout.DIV(
        layout.LABEL(layout.ModelFieldLabel("type"), _class="bx--label"),
        layout.DIV(layout.ModelFieldValue("type"), style="margin-top: 1rem"),
    )
    created = layout.DIV(
        layout.LABEL(_("Created"), _class="bx--label"),
        layout.DIV(
            layout.ModelFieldValue("history.last.history_date.date"),
            " / ",
            layout.ModelFieldValue("history.last.history_user"),
            style="margin-top: 1rem",
        ),
    )

    last_change = layout.DIV(
        layout.LABEL(_("Changed"), _class="bx--label"),
        layout.DIV(
            layout.ModelFieldValue("history.first.history_date.date"),
            " / ",
            layout.ModelFieldValue("history.first.history_user"),
            style="margin-top: 1rem",
        ),
    )

    return layout.grid.Grid(
        R(C(layout.H3(layout.I(layout.ObjectLabel())))),
        R(
            C(active_toggle, width=2, breakpoint="max"),
            C(personnumber, width=2, breakpoint="max"),
            C(persontype, width=2, breakpoint="max"),
            C(created, width=2, breakpoint="max"),
            C(last_change, width=2, breakpoint="max"),
        ),
    )


@registerlayout()
def editnaturalperson_form():
    # fix: alignment of tab content and tab should be on global grid I think
    return layout.tabs.Tabs(
        (
            _("Base data"),
            layout.BaseElement(
                layout.grid.Grid(
                    R(C(layout.H4(_("General Information")))),
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
                                C(F("salutation", widgetattributes={"width": "18rem"})),
                                C(F("title")),
                            ),
                            R(
                                C(),
                                C(F("salutation_letter")),
                            ),
                        ),
                    ),
                ),
                layout.DIV(_class="section-separator-bottom"),
                address_and_relationships(),
            ),
        ),
        revisionstab(),
        container=True,
    )


@registerlayout()
def editlegalperson_form():
    # fix: alignment of tab content and tab should be on global grid I think
    return layout.tabs.Tabs(
        (
            _("Base data"),
            layout.BaseElement(
                layout.grid.Grid(
                    R(C(layout.H4(_("General Information")))),
                    R(
                        C(
                            R(
                                C(F("name")),
                                C(F("name_addition")),
                            ),
                            R(
                                C(F("type")),
                                C(F("preferred_language")),
                            ),
                        ),
                        C(
                            R(
                                C(),
                                C(F("salutation_letter")),
                            ),
                        ),
                    ),
                ),
                layout.DIV(_class="section-separator-bottom"),
                address_and_relationships(),
            ),
        ),
        revisionstab(),
        container=True,
    )


def address_and_relationships():
    return layout.grid.Grid(
        R(
            C(
                R(C(layout.H4(_("Address")))),
                layout.form.FormSetField(
                    "core_postal_list",
                    R(C(F("address", widgetattributes={"rows": 2}))),
                    R(
                        C(F("postcode"), breakpoint="lg", width=4),
                        C(F("city"), breakpoint="lg", width=12),
                    ),
                    R(
                        C(F("country")),
                        C(F("type")),
                    ),
                    can_delete=False,
                    max_num=1,
                    extra=1,
                ),
                _class="section-separator-right",
            ),
            C(
                R(
                    C(layout.H4(_("Relationships"))),
                    _class="section-separator-bottom",
                ),
                R(C(layout.H4(_("Communication Channels")))),
                R(C(layout.H5(_("Phone")))),
                layout.form.FormSetField(
                    "core_phone_list",
                    R(
                        C(F("type"), breakpoint="lg", width=4),
                        C(F("number"), breakpoint="lg", width=12),
                    ),
                    can_delete=False,
                    extra=0,
                ),
                R(C(layout.H5(_("Email")))),
                layout.form.FormSetField(
                    "core_email_list",
                    R(C(F("email"))),
                    can_delete=False,
                    extra=0,
                ),
            ),
            _class="section-separator-bottom",
        ),
        R(C(), C(F("remarks")), style="margin-top: 1rem"),
    )


def revisionstab():
    return (
        _("Revisions"),
        layout.BaseElement(
            layout.datatable.DataTable(
                (
                    (_("Date"), layout.ModelFieldValue("history_date")),
                    (_("User"), layout.ModelFieldValue("history_user")),
                    (
                        _("Change"),
                        layout.ModelFieldValue("get_history_type_display"),
                    ),
                ),
                layout.F(lambda c, e: c["object"].history.all()),
                valueproviderclass=layout.ObjectContext,
            )
        ),
    )


@registerlayout()
def relationshipssettings():
    return layout.BaseElement(
        layout.H3(_("Relationships")),
        layout.datatable.DataTable.from_queryset(
            RelationshipType.objects.all(),
            fields=["name"],
            addurl=reverse_model(
                RelationshipType,
                "add",
                query={"next": reverse("basxconnect.core.views.relationshipssettings")},
            ),
            backurl=reverse("basxconnect.core.views.relationshipssettings"),
        ),
    )


@registerlayout()
def personsettings():
    dist = layout.DIV(style="margin-bottom: 2rem")
    return layout.BaseElement(
        layout.H3(_("Persons")),
        # address type
        generate_term_datatable(_("Address types"), "addresstype"),
        dist,
        generate_term_datatable(_("Address origins"), "addressorigin"),
        dist,
        generate_term_datatable(_("Title"), "title"),
        dist,
        generate_term_datatable(
            _("Correspondence Languages"), "correspondence_language"
        ),
        dist,
        generate_term_datatable(_("Communication Channels"), "communication_channels"),
        dist,
        generate_term_datatable(_("Legal Types"), "legaltype"),
        dist,
    )


@registerlayout()
def editpersonheader():
    return None


@registerlayout()
def generalsettings():
    return layout.BaseElement(
        layout.grid.Grid(
            R(C(F("type"))),
            R(C(F("name"))),
            R(C(F("name_addition"))),
        ),
        layout.form.FormSetField(
            "core_postal_list",
            layout.grid.Grid(
                R(C(F("address"))),
                R(C(F("supplemental_address"))),
                R(
                    C(F("postcode"), breakpoint="lg", width=2),
                    C(F("city"), breakpoint="lg", width=3),
                    C(F("country"), breakpoint="lg", width=3),
                ),
            ),
            can_delete=False,
            max_num=1,
            extra=1,
        ),
        layout.grid.Grid(
            R(
                C(single_item_fieldset("core_phone_list", "number")),
                C(single_item_fieldset("core_fax_list", "number")),
            ),
            R(
                C(
                    single_item_fieldset(
                        "core_email_list",
                        "email",
                    )
                ),
                C(single_item_fieldset("core_web_list", "url")),
            ),
        ),
        layout.form.SubmitButton(_("Save")),
    )


def single_item_fieldset(related_field, fieldname, queryset=None):
    """Helper function to show only a single item of a (foreign-key) related item list"""
    return layout.form.FormSetField(
        related_field,
        F(fieldname),
        formsetinitial={"queryset": queryset},
        can_delete=False,
        max_num=1,
        extra=1,
    )


def generate_term_datatable(title, category_slug):
    """Helper function to display a table for all terms of a certain term"""
    return layout.datatable.DataTable.from_queryset(
        Term.objects.filter(category__slug=category_slug),
        fields=["term"],
        title=title,
        addurl=reverse_model(
            Term,
            "add",
            query={
                "category": Category.objects.get(slug=category_slug).id,
                "next": reverse("basxconnect.core.views.personsettings"),
            },
        ),
        backurl=reverse("basxconnect.core.views.personsettings"),
    )
