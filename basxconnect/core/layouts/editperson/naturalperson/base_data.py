import htmlgenerator as hg
from bread import layout
from bread.layout import ObjectFieldValue
from bread.layout.components.icon import Icon
from django.utils.translation import gettext_lazy as _

import basxconnect.core
import basxconnect.core.layouts.editperson.common.addresses
from basxconnect.core import models
from basxconnect.core.layouts.editperson.common.base_data_building_blocks import (
    person_metadata,
)

R = layout.grid.Row
C = layout.grid.Col
F = layout.form.FormField


def base_data_tab(request):

    return layout.tabs.Tab(
        _("Base data"),
        basxconnect.core.layouts.editperson.common.base_data_building_blocks.grid_inside_tab(
            R(
                personal_data(),
                person_metadata(models.NaturalPerson),
            ),
            contact_details_naturalperson(request),
        ),
    )


def personal_data():
    displayed_fields = [
        basxconnect.core.layouts.editperson.common.base_data_building_blocks.display_field_value(
            field
        )
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
            ObjectFieldValue("deceased"),
            basxconnect.core.layouts.editperson.common.base_data_building_blocks.display_field_value(
                "deceased"
            ),
        ),
        hg.If(
            ObjectFieldValue("deceased"),
            basxconnect.core.layouts.editperson.common.base_data_building_blocks.display_field_value(
                "decease_date"
            ),
        ),
    ]
    return basxconnect.core.layouts.editperson.common.base_data_building_blocks.tile_col_edit_modal_displayed_fields(
        _("Personal Data"),
        models.NaturalPerson,
        "ajax_edit_personal_data",
        Icon("user--profile"),
        displayed_fields,
    )


def contact_details_naturalperson(request):
    return hg.BaseElement(
        R(
            basxconnect.core.layouts.editperson.common.addresses.postals(),
            basxconnect.core.layouts.editperson.common.addresses.numbers(request),
        ),
        R(
            basxconnect.core.layouts.editperson.common.addresses.email(request),
            basxconnect.core.layouts.editperson.common.addresses.urls(request),
        ),
        R(
            basxconnect.core.layouts.editperson.common.base_data_building_blocks.tags(),
            basxconnect.core.layouts.editperson.common.base_data_building_blocks.other(),
        ),
    )
