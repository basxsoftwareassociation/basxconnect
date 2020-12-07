from django.db import models
from django.utils.translation import gettext_lazy as _

from .persons import Person


class RelationshipType(models.Model):
    name = models.CharField(_("Name for relationship type"), max_length=255)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ["name"]
        verbose_name = _("Relationship type")
        verbose_name_plural = _("Relationship types")


class Relationship(models.Model):
    type = models.ForeignKey(RelationshipType, on_delete=models.PROTECT)
    type.verbose_name = _("Type")
    person_a = models.ForeignKey(
        Person, on_delete=models.CASCADE, related_name="relationships_to"
    )
    person_a.verbose_name = _("Person A")
    person_b = models.ForeignKey(
        Person,
        on_delete=models.CASCADE,
        related_name="relationships_from",
    )
    person_b.verbose_name = _("Person B")
    start_date = models.DateField(_("Starts on"), blank=True, null=True)
    end_date = models.DateField(_("Ends on"), blank=True, null=True)

    class Meta:
        verbose_name = _("Relationship")
        verbose_name_plural = _("Relationships")
