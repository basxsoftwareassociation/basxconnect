import htmlgenerator as hg
from bread import layout, menu
from bread.utils.urls import reverse, reverse_model
from django.utils.translation import gettext_lazy as _

from basxconnect.core.models import Category, RelationshipType, Term

R = layout.grid.Row
C = layout.grid.Col
F = layout.form.FormField


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
    dist = hg.DIV(style="margin-bottom: 2rem")
    ret = hg.BaseElement(hg.H3(_("Persons")))
    for category in Category.objects.all():
        ret.append(generate_term_datatable(category.name, category.slug))
        ret.append(dist)
    return ret


def generalsettings(request):
    return hg.BaseElement(
        layout.grid.Grid(
            R(C(F("name"))),
            R(C(F("name_addition"))),
            gutter=False,
        ),
        layout.form.FormsetField(
            "core_postal_list",
            layout.grid.Grid(
                R(C(F("address"))),
                R(
                    C(F("postcode"), breakpoint="sm", width=1),
                    C(F("city"), breakpoint="sm", width=3),
                ),
                R(C(F("country"))),
                gutter=False,
            ),
            can_delete=False,
            max_num=1,
            extra=1,
        ),
        layout.grid.Grid(
            R(
                C(single_item_fieldset("core_phone_list", "number")),
                C(
                    single_item_fieldset(
                        "core_email_list",
                        "email",
                    )
                ),
            ),
            R(
                C(single_item_fieldset("core_web_list", "url")),
                C(),
            ),
            gutter=False,
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
    cat = Category.objects.filter(slug=category_slug).first() or ""
    return layout.datatable.DataTable.from_queryset(
        Term.objects.filter(category__slug=category_slug),
        columns=["term"],
        title=title,
        addurl=reverse_model(
            Term,
            "add",
            query={
                "category": cat.id,
            },
        ),
        preven_automatic_sortingnames=True,
        rowclickaction="edit",
        rowactions=[
            menu.Action(
                js=hg.F(
                    lambda c, e: f'window.location = \'{layout.objectaction(c["row"], "delete")}?next=\' + window.location.pathname + window.location.search',
                ),
                icon="trash-can",
            )
        ],
        backurl=reverse("basxconnect.core.views.personsettings"),
    )
