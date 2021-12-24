import htmlgenerator as hg
from bread import layout as layout
from bread.utils.urls import aslayout
from django.utils.translation import gettext_lazy as _
from dynamic_preferences.forms import global_preference_form_builder

import basxconnect.core.layouts.settings_layout as settings_layout

R = layout.grid.Row
C = layout.grid.Col
F = layout.forms.FormField


@aslayout
def generalsettings(request):

    if request.method == "POST":
        form = global_preference_form_builder(
            preferences=["general__organizationname"]
        )(request.POST, request.FILES)
        if form.is_valid():
            form.update_preferences()
    else:
        form = global_preference_form_builder(
            preferences=["general__organizationname"]
        )()

    return layout.grid.Grid(
        R(C(hg.H3(_("Settings")))),
        R(C(hg.H4(_("General")))),
        R(C(hg.H5(_("Information about our organization")))),
        R(
            C(
                layout.forms.Form(
                    form,
                    hg.BaseElement(F("general__organizationname")),
                    layout.forms.helpers.Submit(),
                    style="max-width: 480px",
                )
            )
        ),
        gutter=False,
    )


@aslayout
def personsettings(request):
    return settings_layout.personsettings(request)


@aslayout
def relationshipssettings(request):
    return settings_layout.relationshipssettings(request)
