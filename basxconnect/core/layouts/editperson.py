from collections import Callable

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

    return hg.DIV(
        layout.grid.Grid(
            R(
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
            ),
            gridmode="full-width",
        ),
        hg.DIV(_class="section-separator-bottom", style="margin-top: 1rem"),
        style="margin-bottom: 2rem",
        _class="no-print",
    )


def editperson_head(request, isreadview):
    if isreadview:
        active_toggle = active_toggle_readview()
    else:
        active_toggle = active_toggle_editview()

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
    return layout.grid.Grid(
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
            C(active_toggle, width=1, breakpoint="md"),
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
            _class="disabled-02" if isreadview else "",
        ),
        style="position: sticky; top: 3rem; z-index: 99; background-color: #fff; margin-bottom: 1rem;",
        gridmode="full-width",
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


def active_toggle_editview():
    active_toggle = layout.toggle.Toggle(None, _("Inactive"), _("Active"))
    active_toggle.input.attributes["id"] = "person_active_toggle"
    active_toggle.input.attributes["hx_trigger"] = "change"
    active_toggle.input.attributes["hx_post"] = hg.F(
        lambda c, e: reverse_lazy("core.person.togglestatus", args=[c["object"].pk])
    )
    active_toggle.input.attributes["checked"] = hg.F(lambda c, e: c["object"].active)
    active_toggle.label.insert(0, _("Person status"))
    active_toggle.label.attributes["_for"] = active_toggle.input.attributes["id"]
    return active_toggle


def active_toggle_readview():
    return hg.DIV(
        layout.helpers.LabelElement(_("Status"), _for=False),
        hg.DIV(hg.C("object.status")),
        _class="bx--form-item",
    )


def style_person(ret):
    ret.tabpanels.attributes["style"] = "padding-left: 0; padding-right: 0; "
    ret[0].attributes[
        "style"
    ] = "padding-left: 2rem; padding-right: 2rem; border-bottom: #f4f4f4 solid;"


def contact_details(request):
    return layout.grid.Grid(
        addresses(),
        R(
            numbers(),
            email(),
            _class="section-separator-bottom",
            style="padding-bottom: 2rem",
        ),
        R(
            urls(),
            categories(),
            _class="section-separator-bottom",
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
        _class="section-separator-right",
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
    return C(hg.H4(_("Categories")), layout.form.FormField("categories"))


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
        _class="section-separator-right",
    )


def other():
    return C(hg.H4(_("Other")), F("remarks"))


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
            _class="section-separator-bottom",
            style="padding-bottom: 2rem",
        ),
    )


def revisionstab(request):
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
    return (
        _("Relationships"),
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
            rowactions=[menu.Delete()],
            backurl=request.get_full_path(),
            preven_automatic_sortingnames=True,
            columns=[
                "type",
                person_a_column(),
                person_b_column(),
                "start_date",
                "end_date",
            ],
        ),
    )


def person_a_column() -> DataTableColumn:
    return DataTableColumn(
        "Person A",
        hg.SPAN(
            person_name("person_a"),
            person_number_in_brackets("person_a"),
            **attributes_for_link_to_person(lambda relationship: relationship.person_a),
        ),
    )


def person_b_column() -> DataTableColumn:
    return DataTableColumn(
        "Person B",
        hg.SPAN(
            person_name("person_b"),
            person_number_in_brackets("person_b"),
            **attributes_for_link_to_person(lambda relationship: relationship.person_b),
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
