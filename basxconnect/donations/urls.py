from bread.utils.urls import default_model_paths

from . import models

urlpatterns = [
    *default_model_paths(models.Donation),
]
