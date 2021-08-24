import htmlgenerator as hg
from bread import layout as layout
from bread.forms.forms import generate_form
from bread.utils.urls import aslayout
from django.utils.translation import gettext_lazy as _

import basxconnect.core.layouts.settings_layout as settings_layout

from .. import models, settings

R = layout.grid.Row
C = layout.grid.Col
F = layout.form.FormField


@aslayout
def generalsettings(request):
    layoutobj = settings_layout.generalsettings(request)
    form = None
    if models.Person.objects.filter(id=settings.OWNER_PERSON_ID).exists():
        form = generate_form(
            request,
            models.LegalPerson,
            layoutobj,
            models.Person.objects.filter(id=settings.OWNER_PERSON_ID).first(),
        )

        if request.method == "POST":
            if form.is_valid():
                form.save()

        content = layout.form.Form(form, layoutobj, style="max-width: 480px")
    else:
        content = (
            _(
                "The django setting BASXCONNECT.OWNER_PERSON_ID needs to be set to an existing person in order to be able to edit this screen"
            ),
        )
    return hg.WithContext(
        layout.grid.Grid(
            R(C(hg.H3(_("Settings")))),
            R(C(hg.H4(_("General")))),
            R(C(hg.H5(_("Information about our organization")))),
            R(C(content)),
            gutter=False,
        ),
        form=form,
    )


@aslayout
def personsettings(request):
    return settings_layout.personsettings(request)


@aslayout
def relationshipssettings(request):
    return settings_layout.relationshipssettings(request)
