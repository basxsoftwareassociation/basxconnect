from django.db import models
from django.utils.translation import gettext_lazy as _

from basxconnect.core.models import Person


class Project(models.Model):
    client = models.ForeignKey(
        Person,
        on_delete=models.CASCADE,
        related_name="projects",
        verbose_name=_("Client"),
    )
    name = models.CharField(_("Project name"), max_length=255)
    description = models.TextField(_("Description"), blank=True)

    def __str__(self):
        return f"{self.name} ({self.client})"

    class Meta:
        verbose_name = _("Project")
        verbose_name_plural = _("Projects")
