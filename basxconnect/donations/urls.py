from bread import menu
from bread.utils.urls import default_model_paths, generate_path, reverse
from django.utils.translation import gettext_lazy as _

from . import models
from .wizards.donationsimport import DonationsImportWizard

urlpatterns = [
    *default_model_paths(models.Donation),
    generate_path(
        DonationsImportWizard.as_view(url_name="importdonations"), "importdonations"
    ),
]

importgroup = menu.Group(_("Imports"), icon="document--import")

menu.registeritem(
    menu.Item(
        menu.Link(
            reverse("importdonations", kwargs={"step": "1"}),
            _("Import contributions"),
        ),
        importgroup,
    )
)
