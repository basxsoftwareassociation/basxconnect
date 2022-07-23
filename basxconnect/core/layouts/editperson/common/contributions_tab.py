from basxbread import layout
from basxbread.utils import Link, ModelHref
from django.shortcuts import get_object_or_404
from django.utils.translation import gettext_lazy as _

from basxconnect.contributions.models import Contribution
from basxconnect.core.layouts.editperson.common import utils
from basxconnect.core.models import Person

R = layout.grid.Row
C = layout.grid.Col


def contributions_tab(request):
    person = get_object_or_404(Person, pk=request.resolver_match.kwargs["pk"])
    return layout.tabs.Tab(
        _("Contributions"),
        utils.grid_inside_tab(
            R(
                utils.tiling_col(
                    layout.datatable.DataTable.from_queryset(
                        person.contributions.all(),
                        columns=[
                            "_import.date",
                            "date",
                            "note",
                            "debitaccount",
                            "creditaccount",
                            "amount_formatted",
                        ],
                        title="",
                        primary_button=layout.button.Button.from_link(
                            Link(
                                href=ModelHref(
                                    Contribution, "add", query={"person": person.id}
                                ),
                                label=_("Add %s") % Contribution._meta.verbose_name,
                            ),
                            icon=layout.icon.Icon("add", size=20),
                        ),
                        backurl=request.get_full_path(),
                        prevent_automatic_sortingnames=True,
                    )
                )
            )
        ),
    )
