from bread import layout
from bread.utils import reverse_model
from django.shortcuts import get_object_or_404
from django.utils.translation import gettext_lazy as _

from basxconnect.contributions.models import Contribution
from basxconnect.core.models import Person

R = layout.grid.Row
C = layout.grid.Col
F = layout.form.FormField


def contributions_tab(request):
    person = get_object_or_404(Person, pk=request.resolver_match.kwargs["pk"])
    return layout.tabs.Tab(
        _("Contributions"),
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
            addurl=reverse_model(
                Contribution,
                "add",
                query={
                    "person": person.id,
                },
            ),
            backurl=request.get_full_path(),
            prevent_automatic_sortingnames=True,
        ),
    )
