import htmlgenerator as hg
from bread import layout as layout
from bread.utils.urls import reverse, reverse_model
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _

from .models import Category, Person, Relationship, RelationshipType, Term

R = layout.grid.Row
C = layout.grid.Col
F = layout.form.FormField

dist = layout.DIV(style="margin-bottom: 2rem")


def editperson_toolbar(request):
    deletebutton = layout.button.Button(
        _("Delete"),
        buttontype="ghost",
        icon="trash-can",
        notext=True,
        **layout.aslink_attributes(
            hg.F(lambda c, e: layout.objectaction(c["object"], "delete"))
        ),
    )
    copybutton = layout.button.Button(
        _("Copy"),
        buttontype="ghost",
        icon="copy",
        notext=True,
        **layout.aslink_attributes(
            hg.F(lambda c, e: layout.objectaction(c["object"], "copy"))
        ),
    )

    return layout.DIV(
        layout.grid.Grid(
            R(
                C(
                    layout.search.Search(placeholder=_("Search person")).withajaxurl(
                        url=reverse_lazy("basxconnect.core.views.searchperson"),
                        queryfieldname="query",
                    ),
                    width=2,
                    breakpoint="md",
                ),
                C(
                    deletebutton,
                    copybutton,
                    layout.button.PrintPageButton(buttontype="ghost"),
                ),
            ),
        ),
        layout.DIV(_class="section-separator-bottom", style="margin-top: 1rem"),
        style="margin-bottom: 2rem",
        _class="no-print",
    )


def editperson_head(request):
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
        layout.LABEL(layout.fieldlabel(Person, "personnumber"), _class="bx--label"),
        layout.DIV(hg.C("object.personnumber"), style="margin-top: 1rem"),
    )
    persontype = layout.DIV(
        layout.LABEL(layout.fieldlabel(Person, "type"), _class="bx--label"),
        layout.DIV(hg.C("object.type"), style="margin-top: 1rem"),
    )
    created = layout.DIV(
        layout.LABEL(_("Created"), _class="bx--label"),
        layout.DIV(
            hg.C("object.history.last.history_date.date"),
            " / ",
            hg.C("object.history.last.history_user"),
            style="margin-top: 1rem",
        ),
    )

    last_change = layout.DIV(
        layout.LABEL(_("Changed"), _class="bx--label"),
        layout.DIV(
            hg.C("object.history.first.history_date.date"),
            " / ",
            hg.C("object.history.first.history_user"),
            style="margin-top: 1rem",
        ),
    )

    return layout.grid.Grid(
        R(C(layout.H3(layout.I(hg.C("object"))))),
        R(
            C(active_toggle, width=1, breakpoint="md"),
            C(personnumber, width=1, breakpoint="md"),
            C(persontype, width=1, breakpoint="md"),
            C(created, width=1, breakpoint="md"),
            C(last_change, width=1, breakpoint="md"),
        ),
    )


def editnaturalperson_form(request):
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
                address_and_relationships(request),
            ),
        ),
        relationshipstab(request),
        revisionstab(request),
        container=True,
    )


def editlegalperson_form(request):
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
                address_and_relationships(request),
            ),
        ),
        relationshipstab(request),
        revisionstab(request),
        container=True,
    )


def editpersonassociation_form(request):
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
                                C(),
                            ),
                            R(
                                C(),
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
                address_and_relationships(request),
            ),
        ),
        relationshipstab(request),
        revisionstab(request),
        container=True,
    )


def address_and_relationships(request):
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
        # R(C(F("categories")), C(F("remarks")), style="margin-top: 1rem"),
        R(C(), C(F("remarks")), style="margin-top: 1rem"),
    )


def revisionstab(request):
    return (
        _("Revisions"),
        layout.BaseElement(
            layout.datatable.DataTable(
                (
                    (_("Date"), layout.FC("row.history_date")),
                    (_("User"), layout.FC("row.history_user")),
                    (_("Change"), layout.FC("row.get_history_type_display")),
                ),
                layout.F(lambda c, e: c["object"].history.all()),
            )
        ),
    )


def relationshipstab(request):
    return (
        _("Relationships"),
        layout.datatable.DataTable.from_model(
            Relationship,
            layout.F(
                lambda c, e: c["object"].relationships_to.all()
                | c["object"].relationships_from.all()
            ),
            title="",
            addurl=reverse_model(
                Relationship,
                "add",
                query={
                    "person_a": request.resolver_match.kwargs["pk"],
                    "person_a_nohide": True,
                },
            ),
            backurl=request.get_full_path(),
        ),
    )


def relationshipssettings(request):
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


def personsettings(request):
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


def generalsettings(request):
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
            },
        ),
        backurl=reverse("basxconnect.core.views.personsettings"),
    )
