import htmlgenerator as hg
from bread import layout, menu, views
from bread.utils.links import Link, ModelHref
from bread.utils.urls import autopath, default_model_paths, model_urlname, reverse
from django.utils.translation import gettext_lazy as _
from django.views.generic import RedirectView

from . import models
from .wizards.contributionsimport import ContributionsImportWizard

urlpatterns = [
    autopath(
        RedirectView.as_view(url=reverse("importcontributions", kwargs={"step": "1"})),
        model_urlname(models.ContributionImport, "add"),
    ),
    *default_model_paths(
        models.ContributionImport,
        browseview=views.BrowseView._with(
            columns=(
                layout.datatable.DataTableColumn(
                    _("Import date"), layout.FC("row.date.date"), None
                ),
                layout.datatable.DataTableColumn(
                    _("Importfile"),
                    hg.BaseElement(
                        layout.FC("row.importfile.name"), layout.FC("row.importfile")
                    ),
                    None,
                ),
                "user",
                "bookingrange",
                "numberofbookings",
                "totalamount",
            ),
        ),
    ),
    *default_model_paths(models.Contribution),
    autopath(
        ContributionsImportWizard.as_view(url_name="importcontributions"),
        "importcontributions",
    ),
]

importgroup = menu.Group(_("Imports"), iconname="document--import")

menu.registeritem(
    menu.Item(
        Link(
            ModelHref(models.ContributionImport, "browse"),
            _("Contributions"),
            iconname="money",
        ),
        importgroup,
    )
)
