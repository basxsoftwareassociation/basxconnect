import htmlgenerator as hg
from bread import layout
from bread.utils import Link, ModelHref, pretty_modelname, reverse
from bread.views import BrowseView
from django.utils.translation import gettext_lazy as _

from basxconnect.core.models import Category, RelationshipType, Term

R = layout.grid.Row
C = layout.grid.Col
F = layout.form.FormField


def relationshipssettings(request):
    return layout.grid.Grid(
        R(C(hg.H3(_("Relationships")))),
        R(
            C(
                layout.datatable.DataTable.from_queryset(
                    RelationshipType.objects.all(),
                    columns=["name"],
                    primary_button=layout.button.Button.fromlink(
                        Link(
                            href=ModelHref(
                                RelationshipType,
                                "add",
                                query={
                                    "next": reverse(
                                        "basxconnect.core.views.settings_views.relationshipssettings"
                                    )
                                },
                            ),
                            label=_("Add %s") % pretty_modelname(RelationshipType),
                        ),
                        icon=layout.icon.Icon("add", size=20),
                    ),
                    rowactions=[
                        Link(
                            label=_("Delete"),
                            href=ModelHref(
                                Term, "delete", kwargs={"pk": hg.C("row.pk")}
                            ),
                            iconname="trash-can",
                        )
                    ],
                    backurl=reverse(
                        "basxconnect.core.views.settings_views.relationshipssettings"
                    ),
                ),
            )
        ),
        gutter=False,
    )


def personsettings(request):
    ret = layout.grid.Grid(R(C(hg.H3(_("Persons")))), gutter=False)
    for category in Category.objects.all():
        ret.append(
            R(
                C(generate_term_datatable(category.name, category.slug)),
                style="margin-bottom: 2rem",
            )
        )
    return ret


def generalsettings(request):
    return hg.BaseElement(
        R(C(F("name"))),
        R(C(F("name_addition"))),
        layout.form.FormsetField.as_plain(
            "core_postal_list",
            hg.BaseElement(
                R(C(F("address"))),
                R(
                    C(F("postcode"), breakpoint="sm", width=1),
                    C(F("city"), breakpoint="sm", width=3),
                ),
                R(C(F("country"))),
            ),
            can_delete=False,
            max_num=1,
            extra=1,
        ),
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
        R(C(layout.helpers.SubmitButton(_("Save")))),
    )


def single_item_fieldset(related_field, fieldname, queryset=None):
    """Helper function to show only a single item of a (foreign-key) related item list"""
    return layout.form.FormsetField.as_plain(
        related_field,
        F(fieldname),
        formsetinitial={"queryset": queryset},
        can_delete=False,
        max_num=1,
        extra=1,
    )


def generate_term_datatable(title, category_slug):
    """Helper function to display a table for all terms of a certain term, currently always returns to the personsettings view"""
    # TODO: make the backurl dynamic to return to current view (needs correct handling in the DataTable code)

    cat = Category.objects.filter(slug=category_slug).first() or ""
    return layout.datatable.DataTable.from_queryset(
        Term.objects.filter(category__slug=category_slug),
        columns=["term"],
        title=title,
        primary_button=layout.button.Button.fromlink(
            Link(
                href=ModelHref(
                    Term,
                    "add",
                    query={
                        "category": cat.id,
                        "next": reverse(
                            "basxconnect.core.views.settings_views.personsettings"
                        ),
                    },
                ),
                label=_("Add %s") % pretty_modelname(Term),
            ),
            icon=layout.icon.Icon("add", size=20),
        ),
        prevent_automatic_sortingnames=True,
        rowclickaction=BrowseView.gen_rowclickaction("edit"),
        rowactions=[
            Link(
                label=_("Delete"),
                href=ModelHref(Term, "delete", kwargs={"pk": hg.C("row.pk")}),
                iconname="trash-can",
            )
        ],
        backurl=reverse("basxconnect.core.views.settings_views.personsettings"),
    )
