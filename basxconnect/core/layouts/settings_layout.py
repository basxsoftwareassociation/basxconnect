import htmlgenerator as hg
from basxbread import layout
from basxbread.utils import Link, ModelHref, reverse
from basxbread.views import BrowseView
from django.utils.translation import gettext_lazy as _

from basxconnect.core.models import RelationshipType, Term, Vocabulary

R = layout.grid.Row
C = layout.grid.Col
F = layout.forms.FormField


def relationshipssettings(request):
    return layout.grid.Grid(
        R(C(hg.H3(_("Relationships")))),
        R(
            C(
                layout.datatable.DataTable.from_queryset(
                    RelationshipType.objects.all(),
                    columns=["name"],
                    primary_button=layout.button.Button.from_link(
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
                            label=_("Add %s") % RelationshipType._meta.verbose_name,
                        ),
                        icon=layout.icon.Icon("add", size=20),
                    ),
                    rowactions=[
                        Link(
                            label=_("Edit"),
                            href=ModelHref(
                                RelationshipType,
                                "edit",
                                kwargs={"pk": hg.C("row.pk")},
                                query={
                                    "next": reverse(
                                        "basxconnect.core.views.settings_views.relationshipssettings"
                                    )
                                },
                            ),
                            iconname="edit",
                        ),
                        Link(
                            label=_("Delete"),
                            href=ModelHref(
                                RelationshipType,
                                "delete",
                                kwargs={"pk": hg.C("row.pk")},
                                query={
                                    "next": reverse(
                                        "basxconnect.core.views.settings_views.relationshipssettings"
                                    )
                                },
                            ),
                            iconname="trash-can",
                        ),
                    ],
                    backurl=reverse(
                        "basxconnect.core.views.settings_views.relationshipssettings"
                    ),
                ),
            )
        ),
        gutter=False,
    )


def generate_term_datatable(title, vocabulary_slug):
    """Helper function to display a table for all terms of a certain term, currently always returns to the personsettings view"""

    cat = Vocabulary.objects.filter(slug=vocabulary_slug).first() or ""
    return layout.datatable.DataTable.from_queryset(
        Term.objects.filter(vocabulary__slug=vocabulary_slug),
        columns=["term"],
        title=title,
        primary_button=layout.button.Button.from_link(
            Link(
                href=ModelHref(
                    Term, "add", query={"vocabulary": cat.id}, return_to_current=True
                ),
                label=_("Add %s") % cat,
            ),
            icon=layout.icon.Icon("add", size=20),
        ),
        prevent_automatic_sortingnames=True,
        rowclickaction=BrowseView.gen_rowclickaction("edit", return_to_current=True),
        rowactions=[BrowseView.deletelink()],
        backurl=reverse("basxconnect.core.views.settings_views.personsettings"),
    )
