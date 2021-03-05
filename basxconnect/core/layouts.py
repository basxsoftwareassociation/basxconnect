import htmlgenerator as hg
from bread import layout
from bread.utils.urls import reverse, reverse_model
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _

from .models import Category, Person, Relationship, RelationshipType, Term

R = layout.grid.Row
C = layout.grid.Col
F = layout.form.FormField

dist = hg.DIV(style="margin-bottom: 2rem")


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

    return hg.DIV(
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
        hg.DIV(_class="section-separator-bottom", style="margin-top: 1rem"),
        style="margin-bottom: 2rem",
        _class="no-print",
    )


def editperson_head(request, isreadview):
    active_toggle = layout.toggle.Toggle(None, _("Inactive"), _("Active"))
    active_toggle.input.attributes["id"] = "person_active_toggle"
    active_toggle.input.attributes["hx_trigger"] = "change"
    active_toggle.input.attributes["hx_post"] = hg.F(
        lambda c, e: reverse_lazy("core.person.togglestatus", args=[c["object"].pk])
    )
    active_toggle.input.attributes["checked"] = hg.F(lambda c, e: c["object"].active)
    active_toggle.label.insert(0, _("Person status"))
    active_toggle.label.attributes["_for"] = active_toggle.input.attributes["id"]

    personnumber = hg.DIV(
        hg.LABEL(layout.fieldlabel(Person, "personnumber"), _class="bx--label"),
        hg.DIV(hg.C("object.personnumber"), style="margin-top: 1rem"),
    )
    personmaintype = hg.DIV(
        hg.LABEL(_("Main Type"), _class="bx--label"),
        hg.DIV(layout.ModelName("object"), style="margin-top: 1rem"),
    )
    persontype = hg.DIV(
        hg.LABEL(layout.fieldlabel(Person, "type"), _class="bx--label"),
        hg.DIV(hg.C("object.type"), style="margin-top: 1rem"),
    )
    created = hg.DIV(
        hg.LABEL(_("Created"), _class="bx--label"),
        hg.DIV(
            hg.C("object.history.last.history_date.date"),
            " / ",
            hg.C("object.history.last.history_user"),
            style="margin-top: 1rem",
        ),
    )

    last_change = hg.DIV(
        hg.LABEL(_("Changed"), _class="bx--label"),
        hg.DIV(
            hg.C("object.history.first.history_date.date"),
            " / ",
            hg.C("object.history.first.history_user"),
            style="margin-top: 1rem",
        ),
    )

    areyousure = layout.modal.Modal(
        _("Unsaved changes"),
        buttons=(
            layout.button.Button(
                _("Discard"),
                buttontype="secondary",
                **layout.aslink_attributes(
                    hg.F(
                        lambda c, e: reverse_model(
                            c["object"], "read", kwargs={"pk": c["object"].pk}
                        )
                    )
                ),
            ),
            layout.button.Button(
                _("Save changes"),
                buttontype="primary",
                onclick="document.querySelector('div.bx--content form[method=POST]').submit()",
            ),
        ),
    )
    view_button_attrs = {}
    if not isreadview:
        view_button_attrs = {
            **areyousure.openerattributes,
        }
    return layout.grid.Grid(
        R(
            C(hg.H3(hg.I(hg.C("object"))), width=12, breakpoint="lg"),
            C(
                layout.content_switcher.ContentSwitcher(
                    ("View", view_button_attrs),
                    (
                        "Edit",
                        layout.aslink_attributes(
                            hg.F(
                                lambda c, e: reverse_model(
                                    c["object"], "edit", kwargs={"pk": c["object"].pk}
                                )
                            )
                        ),
                    ),
                    selected=0 if isreadview else 1,
                    onload=""
                    if isreadview
                    else "this.addEventListener('content-switcher-beingselected', (e) => e.preventDefault())",
                ),
                areyousure,
                width=4,
                breakpoint="lg",
            ),
        ),
        R(
            C(active_toggle, width=1, breakpoint="md"),
            C(personnumber, width=1, breakpoint="md"),
            C(personmaintype, width=1, breakpoint="md"),
            C(persontype, width=1, breakpoint="md"),
            C(created, width=1, breakpoint="md"),
            C(last_change, width=1, breakpoint="md"),
            C(),
            *(
                []
                if isreadview
                else [
                    C(
                        layout.button.Button(
                            _("Save changes"),
                            id=hg.BaseElement("save-button-", hg.C("object.pk")),
                            icon="save",
                            buttontype="ghost",
                            onclick="document.querySelector('div.bx--content form[method=POST]').submit()",
                        ),
                        width=1,
                        breakpoint="md",
                    )
                ]
            ),
        ),
    )


def editnaturalperson_form(request):
    return layout.tabs.Tabs(
        (
            _("Base data"),
            hg.BaseElement(
                layout.grid.Grid(
                    R(C(hg.H4(_("General")))),
                    R(
                        C(
                            R(
                                C(F("salutation")),
                                C(F("title")),
                                C(F("profession")),
                            ),
                            R(
                                C(F("first_name")),
                                C(F("last_name")),
                            ),
                            R(
                                C(F("name")),
                            ),
                        ),
                        C(
                            R(
                                C(width=1, breakpoint="lg"),
                                C(F("form_of_address")),
                                C(F("gender")),
                                C(width=1, breakpoint="lg"),
                                C(F("preferred_language"), width=4, breakpoint="lg"),
                            ),
                            R(
                                C(width=1, breakpoint="lg"),
                                C(F("salutation_letter")),
                                C(width=1, breakpoint="lg"),
                                C(width=4, breakpoint="lg"),
                            ),
                            R(
                                C(width=1, breakpoint="lg"),
                                C(F("date_of_birth"), width=4, breakpoint="lg"),
                                C(),
                                C(
                                    F(
                                        "deceased",
                                        elementattributes={"_class": "standalone"},
                                    )
                                ),
                                C(F("decease_date"), width=4, breakpoint="lg"),
                            ),
                        ),
                    ),
                ),
                hg.DIV(_class="section-separator-bottom"),
                address_and_relationships(request),
            ),
        ),
        relationshipstab(request),
        container=True,
    )


def editlegalperson_form(request):
    # fix: alignment of tab content and tab should be on global grid I think
    return layout.tabs.Tabs(
        (
            _("Base data"),
            hg.BaseElement(
                layout.grid.Grid(
                    R(C(hg.H4(_("General Information")))),
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
                hg.DIV(_class="section-separator-bottom"),
                address_and_relationships(request),
            ),
        ),
        relationshipstab(request),
        container=True,
    )


def editpersonassociation_form(request):
    # fix: alignment of tab content and tab should be on global grid I think
    return layout.tabs.Tabs(
        (
            _("Base data"),
            hg.BaseElement(
                layout.grid.Grid(
                    R(C(hg.H4(_("General Information")))),
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
                hg.DIV(_class="section-separator-bottom"),
                address_and_relationships(request),
            ),
        ),
        relationshipstab(request),
        container=True,
    )


def address_and_relationships(request):
    return layout.grid.Grid(
        R(
            C(
                hg.H4(_("Address")),
                layout.form.FormsetField(
                    "core_postal_list",
                    R(
                        C(F("type")),
                        C(F("address", widgetattributes={"style": "height: 8.5rem"})),
                        C(R(C(F("postcode"))), R(C(F("country")))),
                        C(F("city")),
                        C(
                            layout.form.InlineDeleteButton(".bx--row"),
                            style="margin-top: 1.5rem",
                            breakpoint="lg",
                            width=1,
                        ),
                    ),
                ),
                layout.form.FormsetAddButton("core_postal_list", style="float: right"),
                _class="section-separator-bottom",
                style="padding-bottom: 2rem",
            ),
        ),
        R(
            C(
                hg.H5(_("Numbers")),
                layout.form.FormsetField(
                    "core_phone_list",
                    R(
                        C(F("type"), breakpoint="lg", width=4),
                        C(F("number"), breakpoint="lg", width=12),
                    ),
                ),
                layout.form.FormsetAddButton("core_phone_list", style="float: right"),
                _class="section-separator-right",
            ),
            C(
                hg.H5(_("Email")),
                layout.form.FormsetField(
                    "core_email_list",
                    R(
                        C(F("type"), breakpoint="lg", width=4),
                        C(F("email"), breakpoint="lg", width=12),
                    ),
                ),
                layout.form.FormsetAddButton("core_email_list", style="float: right"),
            ),
            _class="section-separator-bottom",
            style="padding-bottom: 2rem",
        ),
        R(
            C(
                hg.H5(_("URLs")),
                layout.form.FormsetField(
                    "core_web_list",
                    R(
                        C(F("type"), breakpoint="lg", width=4),
                        C(F("url"), breakpoint="lg", width=12),
                    ),
                ),
                layout.form.FormsetAddButton("core_web_list", style="float: right"),
                _class="section-separator-right",
            ),
            C(
                hg.H5(_("Categories")),
            ),
            _class="section-separator-bottom",
            style="padding-bottom: 2rem",
        ),
        R(
            C(hg.H5(_("Other")), F("remarks")),
            C(),
            style="margin-top: 1rem",
        ),
    )


def revisionstab(request):
    return (
        _("Revisions"),
        hg.BaseElement(
            layout.datatable.DataTable(
                columns=(
                    (_("Date"), layout.FC("row.history_date"), None),
                    (_("User"), layout.FC("row.history_user"), None),
                    (_("Change"), layout.FC("row.get_history_type_display"), None),
                ),
                row_iterator=hg.F(lambda c, e: c["object"].history.all()),
            )
        ),
    )


def relationshipstab(request):
    return (
        _("Relationships"),
        layout.datatable.DataTable.from_model(
            Relationship,
            hg.F(
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
            preven_automatic_sortingnames=True,
        ),
    )


def relationshipssettings(request):
    return hg.BaseElement(
        hg.H3(_("Relationships")),
        layout.datatable.DataTable.from_queryset(
            RelationshipType.objects.all(),
            columns=["name"],
            addurl=reverse_model(
                RelationshipType,
                "add",
                query={"next": reverse("basxconnect.core.views.relationshipssettings")},
            ),
            backurl=reverse("basxconnect.core.views.relationshipssettings"),
        ),
    )


def personsettings(request):
    return hg.BaseElement(
        hg.H3(_("Persons")),
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
    return hg.BaseElement(
        layout.grid.Grid(
            R(C(F("type"))),
            R(C(F("name"))),
            R(C(F("name_addition"))),
        ),
        layout.form.FormsetField(
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
        layout.helpers.SubmitButton(_("Save")),
    )


def single_item_fieldset(related_field, fieldname, queryset=None):
    """Helper function to show only a single item of a (foreign-key) related item list"""
    return layout.form.FormsetField(
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
        columns=["term"],
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
