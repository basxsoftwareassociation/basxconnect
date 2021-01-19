from bread.utils.urls import default_model_paths, generate_path

from . import models
from .wizards.donationsimport import DonationsImportWizard

urlpatterns = [
    *default_model_paths(models.Donation),
    generate_path(
        DonationsImportWizard.as_view(url_name="importdonations"), "importdonations"
    ),
]
