import collections
from typing import List, Union

import bread.layout
import htmlgenerator as hg
from bread import layout
from bread.layout import ObjectFieldLabel, ObjectFieldValue
from bread.layout.components.datatable import DataTableColumn
from bread.layout.components.icon import Icon
from bread.layout.components.modal import modal_with_trigger
from bread.layout.components.tag import Tag
from bread.utils import (
    Link,
    ModelHref,
    get_concrete_instance,
    pretty_modelname,
    reverse_model,
)
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from htmlgenerator import Lazy

from basxconnect.core import models
from basxconnect.core.layouts import contributions_tab
from basxconnect.core.layouts.relationshipstab import relationshipstab
from basxconnect.core.models import Person

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

    from django.apps import apps

    return [base_data_tab(request), relationshipstab(request), mailing_tab(request)] + (
        [
            contributions_tab.contributions_tab(request),
        ]
        if apps.is_installed("basxconnect.mailer_integration")
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


def editperson_head(request):
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


def contact_details(request):
    return hg.BaseElement(
        R(
            addresses(),
            numbers(request),
        ),
        R(
            email(request),
            urls(request),
        ),
    )


def numbers(request):
    return tile_with_datatable(
        models.Phone,
        hg.F(lambda c: c["object"].core_phone_list.all()),
        ["type", "number"],
        request,
    )


def tile_with_datatable(model, queryset, fields, request):
    modal = layout.modal.Modal.with_ajax_content(
        _("Add"),
        ModelHref(
            model,
            "add",
            query=hg.F(lambda c: {"person": c["object"].pk, "asajax": True}),
        ),
        submitlabel=_("Save"),
    )
    return tiling_col(
        layout.datatable.DataTable.from_model(
            model,
            queryset,
            prevent_automatic_sortingnames=True,
            columns=fields,
            rowactions=[
                Link(
                    href=ModelHref(
                        model,
                        "edit",
                        kwargs={"pk": hg.C("row.pk")},
                        query={"next": request.get_full_path()},
                    ),
                    iconname="edit",
                    label=_("Edit"),
                ),
                Link(
                    href=ModelHref(
                        model,
                        "delete",
                        kwargs={"pk": hg.C("row.pk")},
                        query={"next": request.get_full_path()},
                    ),
                    iconname="trash-can",
                    label=_("Delete"),
                ),
            ],
            primary_button=layout.button.Button(
                _("Add"), buttontype="primary", **modal.openerattributes
            ),
            style="border-top: none;",
        ),
        modal,
    )


def email(request):
    return tile_with_datatable(
        models.Email,
        hg.F(lambda c: c["object"].core_email_list.all()),
        ["type", "email"],
        request,
    )


def categories():
    return tiling_col(
        hg.H4(_("Categories")),
        hg.Iterator(hg.F(lambda c: c["object"].categories.all()), "i", Tag(hg.C("i"))),
        open_modal_popup_button(
            _("Edit Categories"),
            hg.F(lambda c: get_concrete_instance(c["object"])),
            "ajax_edit_categories",
        ),
    )


def urls(request):
    return tile_with_datatable(
        models.Web,
        hg.F(lambda c: c["object"].core_web_list.all()),
        ["type", "url"],
        request,
    )


def other():
    return tiling_col(
        hg.H4(_("Other")),
        hg.DIV(
            ObjectFieldLabel("remarks"), style="font-weight:bold; margin-bottom: 1rem;"
        ),
        ObjectFieldValue("remarks"),
        open_modal_popup_button(
            "Remarks",
            hg.F(lambda c: get_concrete_instance(c["object"])),
            "ajax_edit_remarks",
        ),
    )


def edit_heading(model: type):
    return _("Edit %s") % pretty_modelname(model)


def display_postal(postal: models.Postal):
    modal = layout.modal.Modal.with_ajax_content(
        heading=edit_heading(models.Postal),
        url=reverse_model(
            models.Postal,
            "ajax_edit",
            kwargs={"pk": postal.pk},
            query={"asajax": True},
        ),
        submitlabel=_("Save"),
    )
    return R(
        C(
            hg.DIV(
                postal.type,
                " (" + _("primary") + ")"
                if postal.person.primary_postal_address
                and postal.person.primary_postal_address.pk == postal.pk
                else "",
                style="font-weight: bold; margin-bottom: 1rem;",
            ),
            hg.DIV(postal.address, style="margin-bottom: 0.25rem;"),
            hg.DIV(postal.postcode, " ", postal.city, style="margin-bottom: 0.25rem;"),
            hg.DIV(postal.get_country_display()),
            hg.DIV(
                edit_postal_button(modal),
                delete_postal_button(postal),
            ),
        ),
        style="margin-top: 1.5rem;",
    )


def edit_postal_button(modal):
    return hg.SPAN(
        layout.button.Button(
            "",
            buttontype="ghost",
            icon="edit",
            **modal.openerattributes,
        ),
        modal,
    )


def delete_postal_button(postal):
    return layout.button.Button(
        _("Delete"),
        buttontype="ghost",
        icon="trash-can",
        notext=True,
        hx_post=reverse_model(
            models.Postal,
            "ajax_delete",
            kwargs={
                "pk": postal.pk,
            },
            query={
                "asajax": True,
            },
        ),
    )


def addresses():
    modal = modal_add_postal()
    return tile_with_icon(
        Icon("map"),
        hg.H4(_("Address(es)")),
        R(
            C(
                hg.Iterator(
                    hg.F(
                        lambda c: getattr(c["object"], "core_postal_list").all()
                        if hasattr(c["object"], "core_postal_list")
                        else []
                    ),
                    "i",
                    hg.BaseElement(
                        hg.F(lambda c: display_postal(c["i"])),
                    ),
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
            lambda c: reverse_model(
                models.Postal,
                "ajax_add",
                query={"asajax": True, "person": c["object"].pk},
            ),
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


def grid_inside_tab(*elems, **attrs):
    attrs = collections.defaultdict(str, attrs or {})
    attrs["style"] += " padding-left: 1rem; padding-right: 1rem"
    return layout.grid.Grid(*elems, **attrs)


def tile_col_edit_modal(
    heading, modal_view: type, action: str, icon: Icon, fields: List[str]
):
    displayed_fields = [display_field_value(field) for field in fields]
    return tile_col_edit_modal_displayed_fields(
        heading, modal_view, action, icon, displayed_fields
    )


def tile_col_edit_modal_displayed_fields(
    heading, model: type, action: str, icon: Icon, displayed_fields: List
):
    return tile_with_icon(
        icon,
        hg.BaseElement(
            hg.H4(heading),
            *displayed_fields,
            open_modal_popup_button(heading, model, action),
        ),
    )


def open_modal_popup_button(heading, model, action):
    return R(
        C(
            modal_with_trigger(
                create_modal(heading, model, action),
                layout.button.Button,
                "Edit",
                buttontype="tertiary",
                icon="edit",
            ),
            style="margin-top: 1.5rem;",
        )
    )


def create_modal(heading, model: Union[type, Lazy], action: str):
    modal = layout.modal.Modal.with_ajax_content(
        heading=heading,
        url=ModelHref(
            model,
            action,
            kwargs={"pk": hg.F(lambda c: c["object"].pk)},
            query={"asajax": True},
        ),
        submitlabel=_("Save"),
    )
    modal[0][1].attributes["style"] = "overflow: visible"
    modal[0].attributes["style"] = "overflow: visible"
    return modal


def tile_header(model, **kwargs):
    return R(
        C(
            hg.H4(
                pretty_modelname(model),
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


def person_metadata(model):
    return tiling_col(
        # we need this to take exactly as much space as a real header
        tile_header(model, style="visibility: hidden;"),
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
