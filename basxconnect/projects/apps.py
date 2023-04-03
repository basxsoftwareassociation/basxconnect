from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class ProjectsConfig(AppConfig):
    name = "basxconnect.projects"
    label = "basxconnect_projects"
    default_auto_field = "django.db.models.BigAutoField"
    verbose_name = _("BasxConnect Projects")
