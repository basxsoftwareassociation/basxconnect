import htmlgenerator as hg
from bread import layout
from bread.layout import ObjectFieldLabel
from bread.layout.components.icon import Icon
from django.utils.translation import gettext_lazy as _

from basxconnect.core import models
from basxconnect.core.layouts.editperson.common import (
    addresses,
    base_data_building_blocks,
)
from basxconnect.core.layouts.editperson.common.base_data_building_blocks import (
    display_label_and_value,
    person_metadata,
)

R = layout.grid.Row
C = layout.grid.Col
F = layout.form.FormField


def base_data_tab(request):

    return layout.tabs.Tab(
        _("Base data"),
        base_data_building_blocks.grid_inside_tab(
            R(
                personal_data(),
                person_metadata(models.NaturalPerson),
            ),
            contact_details_naturalperson(request),
        ),
    )


def personal_data():
    displayed_fields = [
        base_data_building_blocks.display_field_label_and_value(field)
        for field in [
            "salutation",
            "title",
            "name",
            "first_name",
            "last_name",
            "date_of_birth",
            "profession",
        ]
    ] + [
        hg.If(
            hg.C("object.deceased"),
            display_label_and_value(
                ObjectFieldLabel("deceased"),
                hg.If(hg.C("object.deceased"), _("Yes"), _("No")),
            ),
        ),
        hg.If(
            hg.C("object.deceased"),
            base_data_building_blocks.display_field_label_and_value("decease_date"),
        ),
    ]
    return base_data_building_blocks.tile_col_edit_modal_displayed_fields(
        _("Personal Data"),
        models.NaturalPerson,
        "ajax_edit_personal_data",
        Icon("user--profile"),
        displayed_fields,
    )


def contact_details_naturalperson(request):
    return hg.BaseElement(
        R(
            addresses.postals(),
            addresses.numbers(request),
        ),
        R(
            addresses.email(request),
            addresses.urls(request),
        ),
        R(
            base_data_building_blocks.tags(),
            base_data_building_blocks.other(),
        ),
    )
