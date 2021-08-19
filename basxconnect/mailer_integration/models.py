from django.db import models
from django.utils.translation import gettext_lazy as _

from basxconnect.core.models import Person


class Interest(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class MailingPreferences(models.Model):
    person = models.OneToOneField(Person, on_delete=models.CASCADE)
    status = models.CharField(
        max_length=50,
        choices=[
            ("subscribed", "subscribed"),
            ("unsubscribed", "unsubscribed"),
            ("non-subscribed", "non-subscribed"),
            ("cleaned", "cleaned"),
        ],
    )

    interests = models.ManyToManyField(Interest)
    interests.verbose_name = _("Mailing Interests")
