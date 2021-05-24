from typing import Callable

import htmlgenerator as hg
from bread import layout, menu
from bread.layout.components.datatable import DataTableColumn
from bread.utils import reverse_model
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _

from basxconnect.core.models import Person, Relationship

R = layout.grid.Row
C = layout.grid.Col
F = layout.form.FormField


def editperson_form(request, base_data_tab):
    return R(
        C(
            layout.grid.Grid(
                layout.tabs.Tabs(
                    base_data_tab(),
                    relationshipstab(request),
                    container=True,
                    tabpanel_attributes={
                        "_class": "theme-white full-width-white-background",
                    },
                ),
                gutter=False,
            ),
            _class="bx--no-gutter",
        ),
    )


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

    add_person_button = layout.button.Button(
        _("Add person"),
        buttontype="primary",
        icon="add",
        notext=True,
        **layout.aslink_attributes(hg.F(lambda c, e: reverse_model(Person, "add"))),
    )
    return R(
        C(
            layout.search.Search(placeholder=_("Search person")).withajaxurl(
                url=reverse_lazy("basxconnect.core.views.searchperson"),
                query_urlparameter="q",
            ),
            width=2,
            breakpoint="md",
        ),
        C(
            deletebutton,
            copybutton,
            layout.button.PrintPageButton(buttontype="ghost"),
            add_person_button,
        ),
        _class="no-print",
        style="margin-bottom: 1rem;",
    )


def editperson_head(request, isreadview):
    personnumber = hg.DIV(
        hg.LABEL(layout.fieldlabel(Person, "personnumber"), _class="bx--label"),
        hg.DIV(hg.C("object.personnumber"), style="margin-top: 1rem"),
    )
    personmaintype = hg.DIV(
        hg.LABEL(_("Main Type"), _class="bx--label"),
        hg.DIV(layout.ModelName("object"), style="margin-top: 1rem"),
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

    return hg.BaseElement(
        R(
            C(hg.H3(hg.I(hg.C("object"))), width=12, breakpoint="lg"),
            C(
                layout.content_switcher.ContentSwitcher(
                    (_("View"), view_button_attrs),
                    (
                        _("Edit"),
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
            style="padding-top: 1rem",
        ),
        R(
            C(active_toggle(isreadview), width=1, breakpoint="md"),
            C(personnumber, width=1, breakpoint="md"),
            C(personmaintype, width=1, breakpoint="md"),
            C(created, width=1, breakpoint="md"),
            C(last_change(), width=1, breakpoint="md"),
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
                            buttontype="tertiary",
                            onclick="document.querySelector('div.bx--content form[method=POST]').submit()",
                        ),
                        width=4,
                        breakpoint="lg",
                    )
                ]
            ),
        ),
    )


def last_change():
    return hg.DIV(
        hg.LABEL(_("Changed"), _class="bx--label"),
        hg.DIV(
            hg.C("object.history.first.history_date.date"),
            " / ",
            hg.C("object.history.first.history_user"),
            style="margin-top: 1rem",
        ),
    )


def active_toggle(isreadview):
    active_toggle = layout.toggle.Toggle(None, _("Inactive"), _("Active"))
    if isreadview:
        active_toggle.input.attributes["onclick"] = "return false;"
    active_toggle.input.attributes["id"] = "person_active_toggle"
    active_toggle.input.attributes["hx_trigger"] = "change"
    active_toggle.input.attributes["hx_post"] = hg.F(
        lambda c, e: reverse_lazy("core.person.togglestatus", args=[c["object"].pk])
    )
    active_toggle.input.attributes["checked"] = hg.F(lambda c, e: c["object"].active)
    active_toggle.label.insert(0, _("Person status"))
    active_toggle.label.attributes["_for"] = active_toggle.input.attributes["id"]
    return active_toggle


def contact_details():
    return layout.grid.Grid(
        addresses(),
        R(
            numbers(),
            email(),
            style="padding-bottom: 2rem",
        ),
        R(
            urls(),
            categories(),
            style="padding-bottom: 2rem",
        ),
        R(
            other(),
            C(),
            style="margin-top: 1rem",
        ),
        gridmode="full-width",
    )


def numbers():
    return C(
        hg.H4(_("Numbers")),
        layout.form.FormsetField(
            "core_phone_list",
            R(
                C(F("type"), breakpoint="lg", width=4),
                C(
                    F(
                        "number",
                    ),
                    breakpoint="lg",
                    width=8,
                ),
                C(
                    layout.form.InlineDeleteButton(
                        ".bx--row",
                        icon="subtract--alt",
                    ),
                    style="margin-top: 1.5rem",
                    breakpoint="lg",
                    width=2,
                ),
            ),
        ),
        layout.form.FormsetAddButton(
            "core_phone_list",
            buttontype="ghost",
            notext=False,
            label=_("Add number"),
        ),
    )


def email():
    return C(
        hg.H4(_("Email")),
        hg.If(
            hg.F(
                lambda c, e: hasattr(c["object"], "core_email_list")
                and c["object"].core_email_list.count() > 1
            ),
            R(C(F("primary_email_address"), breakpoint="lg", width=4)),
        ),
        layout.form.FormsetField(
            "core_email_list",
            R(
                C(F("type"), breakpoint="lg", width=4),
                C(
                    F(
                        "email",
                    ),
                    breakpoint="lg",
                    width=8,
                ),
                C(
                    layout.form.InlineDeleteButton(
                        ".bx--row",
                        icon="subtract--alt",
                    ),
                    style="margin-top: 1.5rem",
                    breakpoint="lg",
                    width=2,
                ),
            ),
        ),
        layout.form.FormsetAddButton(
            "core_email_list",
            buttontype="ghost",
            notext=False,
            label=_("Add email address"),
        ),
    )


def categories():
    return C(
        hg.H4(_("Categories")),
        layout.form.FormField("categories"),
    )


def urls():
    return C(
        hg.H4(_("URLs")),
        layout.form.FormsetField(
            "core_web_list",
            R(
                C(F("type"), breakpoint="lg", width=4),
                C(
                    F(
                        "url",
                    ),
                    breakpoint="lg",
                    width=8,
                ),
                C(
                    layout.form.InlineDeleteButton(
                        ".bx--row",
                        icon="subtract--alt",
                    ),
                    style="margin-top: 1.5rem",
                    breakpoint="lg",
                    width=2,
                ),
            ),
        ),
        layout.form.FormsetAddButton(
            "core_web_list",
            buttontype="ghost",
            notext=False,
            label=_("Add Url"),
        ),
    )


def other():
    return C(
        hg.H4(_("Other")),
        F("remarks"),
    )


def addresses():
    return R(
        C(
            hg.H4(_("Address(es)")),
            hg.If(
                hg.F(
                    lambda c, e: hasattr(c["object"], "core_postal_list")
                    and c["object"].core_postal_list.count() > 1
                ),
                R(C(F("primary_postal_address"), breakpoint="lg", width=4)),
            ),
            layout.form.FormsetField(
                "core_postal_list",
                R(
                    C(F("type"), width=2, breakpoint="lg"),
                    C(
                        F(
                            "address",
                            widgetattributes={"style": "height: 1rem"},
                        ),
                        width=4,
                        breakpoint="lg",
                    ),
                    C(F("postcode"), width=2, breakpoint="lg"),
                    C(
                        F("city"),
                        width=4,
                        breakpoint="lg",
                    ),
                    C(
                        F("country"),
                        width=3,
                        breakpoint="lg",
                    ),
                    C(
                        layout.form.InlineDeleteButton(
                            ".bx--row",
                            icon="subtract--alt",
                        ),
                        style="margin-top: 1.5rem",
                        breakpoint="lg",
                        width=1,
                    ),
                ),
            ),
            layout.form.FormsetAddButton(
                "core_postal_list",
                buttontype="ghost",
                notext=False,
                label=_("Add address"),
            ),
            style="padding-bottom: 2rem",
        ),
    )


def revisionstab():
    return (
        _("Revisions"),
        hg.BaseElement(
            layout.datatable.DataTable(
                columns=[
                    DataTableColumn(_("Date"), layout.FC("row.history_date")),
                    DataTableColumn(_("User"), layout.FC("row.history_user")),
                    DataTableColumn(
                        _("Change"), layout.FC("row.get_history_type_display")
                    ),
                ],
                row_iterator=hg.F(lambda c, e: c["object"].history.all()),
            )
        ),
    )


def relationshipstab(request):
    return layout.tabs.Tab(
        _("Relationships"),
        layout.grid.Grid(
            R(
                C(
                    layout.datatable.DataTable.from_model(
                        Relationship,
                        hg.F(
                            lambda c, e: c["object"].relationships_to.all()
                            | c["object"].relationships_from.all()
                        ),
                        addurl=reverse_model(
                            Relationship,
                            "add",
                            query={
                                "person_a": request.resolver_match.kwargs["pk"],
                                "person_a_nohide": True,
                            },
                        ),
                        backurl=request.get_full_path(),
                        prevent_automatic_sortingnames=True,
                        columns=[
                            "type",
                            person_in_relationship(
                                "Person A",
                                "person_a",
                                lambda relationship: relationship.person_a,
                            ),
                            person_in_relationship(
                                "Person B",
                                "person_b",
                                lambda relationship: relationship.person_b,
                            ),
                            "start_date",
                            "end_date",
                        ],
                        rowactions=[
                            row_action("delete", "trash-can", _("Delete")),
                            row_action("edit", "edit", _("Edit")),
                        ],
                        rowactions_dropdown=True,
                    )
                )
            ),
            gridmode="narrow",
        ),
    )


def row_action(object_action, icon, label):
    return menu.Action(
        js=hg.F(
            lambda c, e: f'window.location = \'{layout.objectaction(c["row"], object_action)}?next=\' + window.location.pathname + window.location.search',
        ),
        icon=icon,
        label=label,
    )


def person_in_relationship(
    header: str,
    field_name: str,
    get_person: Callable[[Relationship], Person],
) -> DataTableColumn:
    return DataTableColumn(
        header,
        hg.SPAN(
            person_name(field_name),
            person_number_in_brackets(field_name),
            **attributes_for_link_to_person(get_person),
        ),
    )


def attributes_for_link_to_person(get_person: Callable[[Relationship], Person]):
    return layout.aslink_attributes(
        hg.F(
            lambda c, e: reverse_model(
                get_person(c["row"]),
                "read",
                kwargs={"pk": get_person(c["row"]).pk},
            )
        )
    )


def person_name(field):
    return hg.C(f"row.{field}")


def person_number_in_brackets(field):
    return hg.SPAN(" [", hg.C(f"row.{field}.personnumber"), "]")
