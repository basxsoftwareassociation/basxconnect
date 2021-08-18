import htmlgenerator as hg
from bread import layout
from django.utils.translation import gettext_lazy as _

from basxconnect.core.layouts import editperson

R = layout.grid.Row
C = layout.grid.Col
F = layout.form.FormField


def editpersonassociation_form(request):
    return editperson.editperson_form(request, base_data_tab, mailings_tab)


def base_data_tab():
    return layout.tabs.Tab(
        _("Base data"),
        editperson.grid_inside_tab(
            editperson.tiling_row(
                R(
                    C(hg.H4(_("General Information"))),
                ),
                R(
                    C(
                        R(
                            C(F("name"), width=4),
                            C(F("preferred_language"), width=2),
                            C(F("salutation_letter"), width=4),
                        ),
                    ),
                ),
            ),
            editperson.contact_details(),
        ),
    )


def mailings_tab(request):

    from django.apps import apps

    if apps.is_installed("basxconnect.mailer_integration"):
        from basxconnect.mailer_integration.layouts import mailer_integration_tile

        mailer_tile = mailer_integration_tile(request)
    else:
        mailer_tile = editperson.tiling_col()

    return layout.tabs.Tab(
        _("Mailings"),
        editperson.grid_inside_tab(
            R(
                mailer_tile,
                editperson.tiling_col(),
            ),
        ),
    )
