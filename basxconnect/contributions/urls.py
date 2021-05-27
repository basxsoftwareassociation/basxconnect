import htmlgenerator as hg
from bread import layout, menu, views
from bread.utils.urls import (
    default_model_paths,
    generate_path,
    model_urlname,
    reverse,
    reverse_model,
)
from django.utils.translation import gettext_lazy as _
from django.views.generic import RedirectView

from . import models
from .wizards.contributionsimport import ContributionsImportWizard

urlpatterns = [
    generate_path(
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
            bulkactions=(
                menu.Link(
                    reverse_model(models.ContributionImport, "bulkdelete"),
                    label="Delete",
                    icon="trash-can",
                ),
            ),
        ),
    ),
    generate_path(
        views.BulkDeleteView.as_view(model=models.ContributionImport),
        model_urlname(models.ContributionImport, "bulkdelete"),
    ),
    *default_model_paths(models.Contribution),
    generate_path(
        ContributionsImportWizard.as_view(url_name="importcontributions"),
        "importcontributions",
    ),
]

importgroup = menu.Group(_("Imports"), icon="document--import")

menu.registeritem(
    menu.Item(
        menu.Link(
            reverse_model(models.ContributionImport, "browse"),
            _("Contributions"),
        ),
        importgroup,
    )
)
