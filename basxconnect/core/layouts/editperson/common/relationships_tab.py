from typing import Callable

import htmlgenerator as hg
from bread import layout
from bread.layout.components.datatable import DataTableColumn
from bread.utils import Link, ModelHref, reverse_model
from django.shortcuts import get_object_or_404
from django.utils.translation import gettext_lazy as _

from basxconnect.core.layouts.editperson.common import utils
from basxconnect.core.models import Person, Relationship

R = layout.grid.Row
C = layout.grid.Col


def relationshipstab(request):
    person = get_object_or_404(Person, pk=request.resolver_match.kwargs["pk"])
    modal_from = modal_add_relationship_from(person)
    modal_to = modal_add_relationship_to(person)
    return layout.tabs.Tab(
        _("Relationships"),
        utils.grid_inside_tab(
            R(
                utils.tiling_col(
                    relationships_datatable(
                        request,
                        title=_("Relationships to person"),
                        queryset=hg.F(lambda c: c["object"].relationships_from.all()),
                        primary_button=button_add_relationship_to(modal_to),
                    ),
                    modal_to,
                    hg.DIV(style="margin-top: 4rem;"),
                    relationships_datatable(
                        request,
                        title=_("Relationships from person"),
                        queryset=hg.F(lambda c: c["object"].relationships_to.all()),
                        primary_button=button_add_relationship_from(modal_from),
                    ),
                    modal_from,
                )
            ),
        ),
    )


def relationships_datatable(request, queryset, primary_button, title):
    return layout.datatable.DataTable.from_model(
        Relationship,
        queryset,
        title=title,
        backurl=request.get_full_path(),
        prevent_automatic_sortingnames=True,
        columns=[
            person_in_relationship(
                "Person A",
                "person_a",
                lambda relationship: relationship.person_a,
            ),
            "type",
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
                href=ModelHref(
                    Relationship,
                    "edit",
                    kwargs={"pk": hg.C("row.pk")},
                    query={"next": request.get_full_path()},
                ),
                iconname="edit",
                label=_("Edit"),
            ),
            Link(
                href=ModelHref(
                    Relationship,
                    "delete",
                    kwargs={"pk": hg.C("row.pk")},
                    query={"next": request.get_full_path()},
                ),
                iconname="trash-can",
                label=_("Delete"),
            ),
        ],
        primary_button=primary_button,
    )


def button_add_relationship_from(modal):
    return layout.button.Button(
        _("Add relationship from person"),
        **modal.openerattributes,
    )


def button_add_relationship_to(modal):
    return layout.button.Button(
        _("Add relationship to person"),
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
