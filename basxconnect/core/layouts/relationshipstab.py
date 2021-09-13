from typing import Callable

import htmlgenerator as hg
from bread import layout
from bread.layout.components.datatable import DataTableColumn
from bread.utils import Link, ModelHref, reverse_model
from django.shortcuts import get_object_or_404
from django.utils.translation import gettext_lazy as _

from basxconnect.core.models import Person, Relationship

R = layout.grid.Row
C = layout.grid.Col


def relationshipstab(request):
    person = get_object_or_404(Person, pk=request.resolver_match.kwargs["pk"])
    modal_from = modal_add_relationship_from(person)
    modal_to = modal_add_relationship_to(person)
    label = _("Edit")
    label1 = _("Delete")
    return layout.tabs.Tab(
        _("Relationships"),
        hg.BaseElement(
            layout.datatable.DataTable.from_model(
                Relationship,
                hg.F(lambda c: c["object"].relationships_from.all()),
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
                    Link(
                        href="#",
                        iconname="edit",
                        label=label,
                        modal=generate_modal_edit_relationship,
                    ),
                    row_action("delete", "trash-can", _("Delete")),
                ],
                primary_button=button_add_relationship_to(modal_to),
            ),
            modal_to,
            layout.datatable.DataTable.from_model(
                Relationship,
                hg.F(lambda c: c["object"].relationships_to.all()),
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
                    Link(
                        href="#",
                        iconname="edit",
                        label=label,
                        modal=generate_modal_edit_relationship,
                    ),
                    row_action("delete", "trash-can", _("Delete")),
                ],
                primary_button=button_add_relationship_from(modal_from),
            ),
            modal_from,
        ),
    )


def button_add_relationship_from(modal):
    return layout.button.Button(
        _("Add relationship from person"),
        buttontype="primary",
        **modal.openerattributes,
    )


def button_add_relationship_to(modal):
    return layout.button.Button(
        _("Add relationship to person"),
        buttontype="primary",
        **modal.openerattributes,
    )


def modal_add_relationship_from(person):
    ret = layout.modal.Modal.with_ajax_content(
        heading=_("Add relationship from person"),
        url=ModelHref(
            Relationship, "add", query={"asajax": True, "person_a": person.pk}
        ),
        submitlabel=_("Save"),
    )
    return ret


def modal_add_relationship_to(person):
    ret = layout.modal.Modal.with_ajax_content(
        heading=_("Add relationship to person"),
        url=ModelHref(
            Relationship, "add", query={"asajax": True, "person_b": person.pk}
        ),
        submitlabel=_("Save"),
    )
    return ret


def generate_modal_edit_relationship():
    ret = layout.modal.Modal.with_ajax_content(
        heading=_("Edit relationship of person"),
        url=ModelHref(
            Relationship, "edit", query={"asajax": True}, kwargs={"pk": hg.C("row.pk")}
        ),
        submitlabel=_("Save"),
    )
    return ret


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
            lambda c: reverse_model(
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


def row_action(object_action, icon, label):
    return Link(
        href=ModelHref(Relationship, object_action, kwargs={"pk": hg.C("row.pk")}),
        iconname=icon,
        label=label,
    )
