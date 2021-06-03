import htmlgenerator as hg
from bread import layout, menu
from bread.layout.components.datatable import DataTableColumn
from bread.utils import reverse_model
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _

from basxconnect.core.models import Person, Relationship

R = layout.grid.Row
C = layout.grid.Col
F = layout.form.FormField

def contributions_tab():
    return layout.tabs.Tab(
        _("Relationships"),
        layout.grid.Grid(
            R(
                C("Hello World")
            ),
            gutter=False,
        ),
    )
