import collections

import bread.layout
import htmlgenerator as hg
from bread import layout
from bread.layout.components.datatable import DataTableColumn
from bread.utils import reverse, reverse_model
from bread.utils.links import Link, ModelHref
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _

import basxconnect.core.settings
from basxconnect.core.layouts import contributions_tab
from basxconnect.core.models import Person, Relationship
from basxconnect.core.views.person import search_person_view

R = layout.grid.Row
C = layout.grid.Col
F = layout.form.FormField


def editperson_form(request, base_data_tab, mailings_tab):
    return R(
        C(
            layout.grid.Grid(
                layout.tabs.Tabs(
                    *editperson_tabs(base_data_tab, mailings_tab, request),
                    tabpanel_attributes={
                        "_class": "tile-container",
                        "style": "padding: 0;",
                    },
                    labelcontainer_attributes={
                        "_class": "tabs-lg",
                        "style": "background-color: white;",
                    },
                ),
                gutter=False,
            ),
        ),
    )


def editperson_tabs(base_data_tab, mailing_tab, request):
    return [base_data_tab(), relationshipstab(request), mailing_tab(request)] + (
        [
            contributions_tab.contributions_tab(request),
        ]
        if basxconnect.core.settings.ENABLE_CONTRIBUTIONS
        else []
    )


def editperson_toolbar(request):
    deletebutton = layout.button.Button(
        _("Delete"),
        buttontype="ghost",
        icon="trash-can",
        notext=True,
        **layout.aslink_attributes(
            hg.F(lambda c: layout.objectaction(c["object"], "delete"))
        ),
    )
    restorebutton = layout.button.Button(
        _("Restore"),
        buttontype="ghost",
        icon="undo",
        notext=True,
        **layout.aslink_attributes(
            hg.F(
                lambda c: layout.objectaction(
                    c["object"], "delete", query={"restore": True}
                )
            )
        ),
    )
    copybutton = layout.button.Button(
        _("Copy"),
        buttontype="ghost",
        icon="copy",
        notext=True,
        **layout.aslink_attributes(
            hg.F(lambda c: layout.objectaction(c["object"], "copy"))
        ),
    )

    add_person_button = layout.button.Button(
        _("Add person"),
        buttontype="primary",
        icon="add",
        notext=True,
        **layout.aslink_attributes(hg.F(lambda c: reverse_model(Person, "add"))),
    )
    return hg.SPAN(
        hg.If(hg.C("object.deleted"), restorebutton, deletebutton),
        copybutton,
        layout.button.PrintPageButton(buttontype="ghost"),
        add_person_button,
        _class="no-print",
        style="margin-bottom: 1rem; margin-left: 1rem",
        width=3,
    )


def editperson_head(request, isreadview):
    personnumber = hg.DIV(
        hg.LABEL(layout.fieldlabel(Person, "personnumber"), _class="bx--label"),
        hg.DIV(hg.C("object.personnumber"), style="margin-top: 1rem"),
        style="margin-left: 2rem",
    )
    personmaintype = hg.DIV(
        hg.LABEL(_("Main Type"), _class="bx--label"),
        hg.DIV(layout.ModelName("object"), style="margin-top: 1rem;"),
        style="margin-left: 2rem",
    )
    created = hg.DIV(
        hg.LABEL(_("Created"), _class="bx--label"),
        hg.DIV(
            hg.C("object.history.last.history_date.date"),
            " / ",
            hg.C("object.history.last.history_user"),
            style="margin-top: 1rem",
        ),
        style="margin-left: 2rem",
    )

    areyousure = layout.modal.Modal(
        _("Unsaved changes"),
        buttons=(
            layout.button.Button(
                _("Discard"),
                buttontype="secondary",
                **layout.aslink_attributes(
                    hg.F(
                        lambda c: reverse_model(
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
            C(
                hg.H3(
                    hg.SPAN(
                        hg.C("object"),
                        style=hg.If(
                            hg.C("object.deleted"), "text-decoration: line-through"
                        ),
                    ),
                    editperson_toolbar(request),
                ),
                width=12,
            ),
            C(
                layout.content_switcher.ContentSwitcher(
                    (_("View"), view_button_attrs),
                    (
                        _("Edit"),
                        layout.aslink_attributes(
                            hg.F(
                                lambda c: reverse_model(
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
            ),
            style="padding-top: 1rem",
        ),
        R(
            C(
                hg.DIV(
                    active_toggle(isreadview),
                    personnumber,
                    personmaintype,
                    created,
                    last_change(),
                    style="display:flex;",
                ),
                width=9,
            ),
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
                        _class="bx--offset-lg-3",
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
        style=" margin-left: 2rem",
    )


def active_toggle(isreadview):
    active_toggle = layout.toggle.Toggle(None, _("Inactive"), _("Active"))
    if isreadview:
        active_toggle.input.attributes["onclick"] = "return false;"
    active_toggle.input.attributes["id"] = "person_active_toggle"
    active_toggle.input.attributes["hx_trigger"] = "change"
    active_toggle.input.attributes["hx_post"] = hg.F(
        lambda c: reverse_lazy("core.person.togglestatus", args=[c["object"].pk])
    )
    active_toggle.input.attributes["checked"] = hg.F(lambda c: c["object"].active)
    active_toggle.label.insert(0, _("Person status"))
    active_toggle.label.attributes["_for"] = active_toggle.input.attributes["id"]
    return hg.DIV(active_toggle)


def contact_details():
    return hg.BaseElement(
        addresses(),
        R(
            numbers(),
            email(),
        ),
        R(
            urls(),
            other(),
        ),
    )


def numbers():
    return tiling_col(
        hg.H4(_("Numbers")),
        layout.form.FormsetField.as_plain(
            "core_phone_list",
            R(
                C(F("type"), width=4),
                C(F("number"), width=8),
                C(
                    layout.form.InlineDeleteButton(
                        ".bx--row",
                        icon="subtract--alt",
                    ),
                    style="margin-top: 1.5rem",
                    width=2,
                ),
            ),
            add_label=_("Add number"),
        ),
    )


def email():
    return tiling_col(
        hg.H4(_("Email")),
        hg.If(
            hg.F(
                lambda c: hasattr(c["object"], "core_email_list")
                and c["object"].core_email_list.count() > 1
            ),
            R(C(F("primary_email_address"), width=4)),
        ),
        layout.form.FormsetField.as_plain(
            "core_email_list",
            R(
                C(F("type"), width=4),
                C(F("email"), width=8),
                C(
                    layout.form.InlineDeleteButton(
                        ".bx--row",
                        icon="subtract--alt",
                    ),
                    style="margin-top: 1.5rem",
                    width=2,
                ),
            ),
            add_label=_("Add email address"),
        ),
    )


def categories():
    return tiling_col(
        hg.H4(_("Categories")),
        layout.form.FormField("categories"),
    )


def urls():
    return tiling_col(
        hg.H4(_("URLs")),
        layout.form.FormsetField.as_plain(
            "core_web_list",
            R(
                C(F("type"), width=4),
                C(F("url"), width=8),
                C(
                    layout.form.InlineDeleteButton(
                        ".bx--row",
                        icon="subtract--alt",
                    ),
                    style="margin-top: 1.5rem",
                    width=2,
                ),
            ),
            add_label=_("Add Url"),
        ),
    )


def other():
    return tiling_col(
        hg.H4(_("Other")),
        F("remarks"),
    )


def addresses():
    return tiling_row(
        hg.H4(_("Address(es)")),
        hg.If(
            hg.F(
                lambda c: hasattr(c["object"], "core_postal_list")
                and c["object"].core_postal_list.count() > 1
            ),
            R(C(F("primary_postal_address"), width=4)),
        ),
        layout.form.FormsetField.as_plain(
            "core_postal_list",
            R(
                C(F("type"), width=2),
                C(
                    F(
                        "address",
                        widgetattributes={"style": "height: 1rem"},
                    ),
                    width=4,
                ),
                C(F("postcode"), width=2),
                C(F("city"), width=4),
                C(F("country"), width=3),
                C(
                    layout.form.InlineDeleteButton(
                        ".bx--row",
                        icon="subtract--alt",
                    ),
                    style="margin-top: 1.5rem",
                    width=1,
                ),
            ),
            add_label=_("Add address"),
        ),
        style="padding-bottom: 2rem",
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
                row_iterator=hg.F(lambda c: c["object"].history.all()),
            )
        ),
    )


def relationshipstab(request):
    return layout.tabs.Tab(
        _("Relationships"),
        hg.BaseElement(
            layout.form.FormsetField.as_datatable(
                "relationships_to",
                [
                    layout.datatable.DataTableColumn(
                        layout.fieldlabel(Relationship, "person_a"),
                        hg.C("object"),
                    ),
                    "type",
                    layout.datatable.DataTableColumn(
                        layout.fieldlabel(Relationship, "person_b"),
                        F(
                            "person_b",
                            fieldtype=layout.search_select.SearchSelect,
                            hidelabel=True,
                            elementattributes={
                                "backend": layout.search.SearchBackendConfig(
                                    reverse_lazy(
                                        "basxconnect.core.views.person.search_person_view.searchperson"
                                    ),
                                    result_selector=f".{search_person_view.ITEM_CLASS}",
                                    result_label_selector=f".{search_person_view.ITEM_LABEL_CLASS}",
                                    result_value_selector=f".{search_person_view.ITEM_VALUE_CLASS}",
                                ),
                            },
                        ),
                    ),
                    "start_date",
                    "end_date",
                ],
                # String-formatting with lazy values does not yet work in htmlgenerator but would be nice to have
                # see https://github.com/basxsoftwareassociation/htmlgenerator/issues/6
                title=hg.F(
                    lambda c: _('Relationships from %s to "person B"') % c["object"]
                ),
            ),
            layout.form.FormsetField.as_datatable(
                "relationships_from",
                [
                    layout.datatable.DataTableColumn(
                        layout.fieldlabel(Relationship, "person_a"),
                        F(
                            "person_a",
                            fieldtype=layout.search_select.SearchSelect,
                            hidelabel=True,
                            elementattributes={
                                "backend": layout.search.SearchBackendConfig(
                                    reverse_lazy(
                                        "basxconnect.core.views.person.search_person_view.searchperson"
                                    ),
                                    result_selector=f".{search_person_view.ITEM_CLASS}",
                                    result_label_selector=f".{search_person_view.ITEM_LABEL_CLASS}",
                                    result_value_selector=f".{search_person_view.ITEM_VALUE_CLASS}",
                                ),
                            },
                        ),
                    ),
                    "type",
                    layout.datatable.DataTableColumn(
                        layout.fieldlabel(Relationship, "person_b"),
                        hg.C("object"),
                    ),
                    "start_date",
                    "end_date",
                ],
                rowactions=[
                    row_action("delete", "trash-can", _("Delete")),
                    row_action("edit", "edit", _("Edit")),
                ],
                rowactions_dropdown=True,
                title=hg.F(
                    lambda c: _('Relationships from "person A" to %s') % c["object"]
                ),
            ),
        ),
    )


def row_action(object_action, icon, label):
    return Link(
        href=ModelHref(Relationship, object_action, kwargs={"pk": hg.C("row.pk")}),
        iconname=icon,
        label=label,
    )


def grid_inside_tab(*elems, **attrs):
    attrs = collections.defaultdict(str, attrs or {})
    attrs["style"] += " padding-left: 1rem; padding-right: 1rem"
    return layout.grid.Grid(*elems, **attrs)


def tile_col_with_edit_modal(modal_view):
    modal = layout.modal.Modal.with_ajax_content(
        heading=modal_view.edit_heading(),
        url=hg.F(
            lambda c: reverse(
                modal_view.path(),
                kwargs={"pk": c["object"].pk},
                query={"asajax": True},
            )
        ),
        submitlabel=_("Save"),
    )
    displayed_fields = [display_field_value(field) for field in modal_view.fields]
    return tile_with_icon(
        modal_view.icon(),
        C(
            R(
                C(
                    hg.H4(
                        modal_view.read_heading(),
                        style="margin-top: 0; margin-bottom: 3rem;",
                    )
                )
            ),
            *displayed_fields,
            R(
                C(
                    layout.button.Button(
                        "Edit",
                        buttontype="tertiary",
                        icon="edit",
                        **modal.openerattributes,
                    ),
                    modal,
                ),
                style="margin-top: 1.5rem;",
            ),
        ),
    )


def tile_with_icon(icon, content):
    return tiling_col(R(C(icon, width=2), content))


def display_field_value(field):
    return R(
        C(
            hg.DIV(
                bread.layout.ObjectFieldLabel(field),
                style="font-weight: bold;",
            ),
            width=6,
        ),
        C(bread.layout.ObjectFieldValue(field)),
        style="padding-bottom: 1.5rem;",
    )


def tiling_col(*elems, **attrs):
    attrs = collections.defaultdict(str, attrs or {})
    attrs["_class"] += " tile tile-col theme-white"
    return C(*elems, **attrs)


def tiling_row(*elems, **attrs):
    attrs = collections.defaultdict(str, attrs or {})
    return R(C(*elems, **attrs), _class="tile theme-white")
