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


def mailings_tab():
    """
    we assume person associations will have mailing-related data (like mailchimp subscription statuses) as well in the
    future and therefore already add an empty tab in order to keep the different types of persons as similar to each
    other as possible.
    """
    return layout.tabs.Tab(
        _("Mailings"),
        editperson.grid_inside_tab(
            R(
                editperson.tiling_col(),
                editperson.tiling_col(),
            ),
            id="mailing-tab-content",
        ),
    )
