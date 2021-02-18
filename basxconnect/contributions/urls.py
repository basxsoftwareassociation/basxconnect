from bread import menu, views
from bread.utils.urls import default_model_paths, generate_path, model_urlname, reverse
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
        browseview=views.BrowseView._with(fields=["date", "importfile"]),
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
            reverse(model_urlname(models.ContributionImport, "browse")),
            _("Contribution imports"),
        ),
        importgroup,
    )
)
