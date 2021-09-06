import collections

import bread.layout
import htmlgenerator as hg
from bread import layout
from bread.layout.components.datatable import DataTableColumn
from bread.layout.components.icon import Icon
from bread.utils import reverse, reverse_model
from bread.utils.links import Link, ModelHref
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _

import basxconnect.core.settings
from basxconnect.core import models
from basxconnect.core.layouts import contributions_tab
from basxconnect.core.models import Person, Relationship
from basxconnect.core.views.person import search_person_view
from basxconnect.core.views.person.person_modals_views import (
    AddPostalAddressView,
    EditPostalAddressView,
)

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
    return [base_data_tab(), relationshipstab(), mailing_tab(request)] + (
        [
            contributions_tab.contributions_tab(request),
        ]
        if basxconnect.core.settings.ENABLE_CONTRIBUTIONS
        else []
    )


def editperson_toolbar(request, isreadview):
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
        *(
            []
            if isreadview
            else [
                layout.button.Button(
                    _("Save changes"),
                    id=hg.BaseElement("save-button-", hg.C("object.pk")),
                    icon="save",
                    buttontype="tertiary",
                    onclick="document.querySelector('div.bx--content form[method=POST]').submit()",
                    style="margin-left: 1rem;",
                ),
            ]
        ),
        _class="no-print",
        style="margin-bottom: 1rem; margin-left: 1rem",
        width=3,
    )


def editperson_head(request, isreadview):
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
                    editperson_toolbar(request, isreadview),
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


def active_toggle_without_label():
    active_toggle = layout.toggle.Toggle(
        None, _("Inactive"), _("Active"), style="margin-top:-1rem; margin-bottom:0;"
    )
    active_toggle.input.attributes["id"] = "person_active_toggle2"
    active_toggle.input.attributes["hx_trigger"] = "change"
    active_toggle.input.attributes["hx_post"] = hg.F(
        lambda c: reverse_lazy("core.person.togglestatus", args=[c["object"].pk])
    )
    active_toggle.input.attributes["checked"] = hg.F(lambda c: c["object"].active)
    active_toggle.label.attributes["_for"] = active_toggle.input.attributes["id"]
    return hg.DIV(active_toggle)


def contact_details():
    return hg.BaseElement(
        R(
            addresses(),
            numbers(),
        ),
        R(
            email(),
            urls(),
        ),
        R(other(), C(width=8)),
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


def display_postal(postal: models.Postal):
    modal = layout.modal.Modal.with_ajax_content(
        heading=EditPostalAddressView.edit_heading(),
        url=reverse(
            EditPostalAddressView.path(),
            kwargs={"pk": postal.pk},
            query={"asajax": True},
        ),
        submitlabel=_("Save"),
    )  # TODO supply the pk of the postal, not the one of the person
    return R(
        C(
            hg.DIV(
                postal.type,
                style="font-weight: bold; margin-bottom: 1rem;",
            ),
            hg.DIV(postal.address, style="margin-bottom: 0.25rem;"),
            hg.DIV(postal.postcode, " ", postal.city, style="margin-bottom: 0.25rem;"),
            hg.DIV(postal.get_country_display()),
            edit_postal_button(modal),
        ),
        style="margin-top: 1.5rem;",
    )


def edit_postal_button(modal):
    return hg.DIV(
        layout.button.Button(
            "",
            buttontype="ghost",
            icon="edit",
            **modal.openerattributes,
        ),
        modal,
    )


def addresses():
    modal = modal_add_postal()
    return tile_with_icon(
        Icon("map"),
        hg.H4(_("Address(es)")),
        hg.If(
            hg.F(
                lambda c: hasattr(c["object"], "core_postal_list")
                and c["object"].core_postal_list.count() > 1
            ),
            hg.BaseElement(
                R(C(F("primary_postal_address"), width=10)),
            ),
        ),
        R(
            C(
                hg.Iterator(
                    hg.F(
                        lambda c: getattr(c["object"], "core_postal_list").all()
                        if hasattr(c["object"], "core_postal_list")
                        else []
                    ),
                    "i",
                    hg.F(lambda c: display_postal(c["i"])),
                )
            )
        ),
        R(
            C(
                layout.button.Button(
                    "Add",
                    buttontype="ghost",
                    icon="Add",
                    **modal.openerattributes,
                ),
                modal,
            ),
            style="margin-top: 1.5rem;",
        ),
    )


def modal_add_postal():
    return layout.modal.Modal.with_ajax_content(
        heading=_("Add Address"),
        url=hg.F(
            lambda c: reverse(
                AddPostalAddressView.path(),
                query={"asajax": True, "person": c["object"].pk},
            )
        ),
        submitlabel=_("Save"),
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


def relationshipstab():
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


def tile_col_edit_modal(modal_view):
    displayed_fields = [display_field_value(field) for field in modal_view.fields]
    return tile_col_edit_modal_selected_fields(modal_view, displayed_fields)


def tile_col_edit_modal_selected_fields(modal_view, displayed_fields):
    modal = create_modal(modal_view)
    return tile_with_icon(
        modal_view.icon(),
        hg.BaseElement(
            tile_header(modal_view.read_heading()),
            *displayed_fields,
            open_modal_popup_button(modal),
        ),
    )


def open_modal_popup_button(modal):
    return R(
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
    )


def create_modal(modal_view):
    return layout.modal.Modal.with_ajax_content(
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


def tile_header(header, **kwargs):
    return R(
        C(
            hg.H4(
                header,
                style="margin-top: 0; margin-bottom: 3rem;",
            ),
            **kwargs,
        )
    )


def tile_with_icon(icon, *content):
    return tiling_col(R(C(icon, width=2), C(*content)))


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


def display_label_and_value(label, value):
    return R(
        C(
            hg.DIV(
                label,
                style="font-weight: bold;",
            ),
            width=6,
        ),
        C(value),
        style="padding-bottom: 1.5rem;",
    )


def tiling_col(*elems, **attrs):
    attrs = collections.defaultdict(str, attrs or {})
    attrs["_class"] += " tile tile-col theme-white"
    return C(*elems, **attrs)


def tiling_row(*elems, **attrs):
    attrs = collections.defaultdict(str, attrs or {})
    return R(C(*elems, **attrs), _class="tile theme-white")


def person_metadata():
    return tiling_col(
        # we need this to take exactly as much space as a real header
        tile_header("A", style="visibility: hidden;"),
        display_field_value("personnumber"),
        display_field_value("maintype"),
        display_label_and_value(_("Status"), active_toggle_without_label()),
        display_label_and_value(
            _("Changed"),
            hg.BaseElement(
                hg.C("object.history.first.history_date.date"),
                " / ",
                hg.C("object.history.first.history_user"),
            ),
        ),
        display_label_and_value(
            _("Created"),
            hg.BaseElement(
                hg.C("object.history.last.history_date.date"),
                " / ",
                hg.C("object.history.last.history_user"),
            ),
        ),
        style="border-left: none;",
    )
