from django.db import models
from django.utils.translation import gettext_lazy as _

from basxconnect.core.models import Email


class Interest(models.Model):
    name = models.CharField(max_length=100, unique=True)
    external_id = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class MailingPreferences(models.Model):
    email = models.OneToOneField(Email, on_delete=models.CASCADE)
    status = models.CharField(
        max_length=50,
        choices=[
            ("subscribed", "subscribed"),
            ("unsubscribed", "unsubscribed"),
            ("non-subscribed", "non-subscribed"),
            ("cleaned", "cleaned"),
        ],
    )

    interests = models.ManyToManyField(Interest, blank=True)
    interests.verbose_name = _("Mailing Interests")
