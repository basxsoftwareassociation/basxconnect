import collections
from typing import List, Union

import htmlgenerator as hg
from bread import layout
from bread.layout import ObjectFieldLabel, ObjectFieldValue
from bread.layout.components.icon import Icon
from bread.layout.components.modal import modal_with_trigger
from bread.utils import ModelHref
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from htmlgenerator import Lazy

R = layout.grid.Row
C = layout.grid.Col
F = layout.form.FormField


def person_metadata():
    return tiling_col(
        # we need this to take exactly as much space as a real header
        hg.DIV("", style="margin-bottom:3.25rem;"),
        display_field_label_and_value("personnumber"),
        display_field_label_and_value("maintype"),
        display_label_and_value(_("Status"), active_toggle()),
        display_label_and_value(
            _("Changed"),
            hg.BaseElement(
                ObjectFieldValue("history.first.history_date.date"),
                " / ",
                hg.C("object.history.first.history_user"),
            ),
        ),
        display_label_and_value(
            _("Created"),
            hg.BaseElement(
                ObjectFieldValue("history.last.history_date.date"),
                " / ",
                hg.C("object.history.last.history_user"),
            ),
        ),
        style="border-left: none;",
    )


def active_toggle():
    toggle = layout.toggle.Toggle(
        None, _("Inactive"), _("Active"), style="margin-top:-1rem; margin-bottom:0;"
    )
    toggle.input.attributes["id"] = "person_active_toggle2"
    toggle.input.attributes["hx_trigger"] = "change"
    toggle.input.attributes["hx_post"] = hg.F(
        lambda c: reverse_lazy("core.person.togglestatus", args=[c["object"].pk])
    )
    toggle.input.attributes["checked"] = hg.F(lambda c: c["object"].active)
    toggle.label.attributes["_for"] = toggle.input.attributes["id"]
    return hg.DIV(toggle)


def grid_inside_tab(*elems, **attrs):
    attrs = collections.defaultdict(str, attrs or {})
    attrs["style"] += " padding-left: 1rem; padding-right: 1rem"
    return layout.grid.Grid(*elems, **attrs)


def tile_col_edit_modal(
    heading, modal_view: type, action: str, icon: Icon, fields: List[str]
):
    displayed_fields = [display_field_label_and_value(field) for field in fields]
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
                _("Edit"),
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
    return modal


def tile_with_icon(icon, *content):
    return tiling_col(R(C(icon, width=2), C(*content)))


def display_field_label_and_value(field):
    return display_label_and_value(ObjectFieldLabel(field), ObjectFieldValue(field))


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
