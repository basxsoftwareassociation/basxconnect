from bread import menu
from bread.utils.urls import default_model_paths, generate_path, reverse
from django.utils.translation import gettext_lazy as _

from . import models
from .wizards.contributionsimport import ContributionsImportWizard

urlpatterns = [
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
            reverse("importcontributions", kwargs={"step": "1"}),
            _("Import contributions"),
        ),
        importgroup,
    )
)
