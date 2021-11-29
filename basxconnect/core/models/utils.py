import datetime

from django.contrib.auth import get_user_model
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.utils.html import mark_safe
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _


class Vocabulary(models.Model):
    name = models.CharField(_("Name"), max_length=255, unique=True)
    slug = models.SlugField(
        _("Slug"),
        unique=True,
        help_text=_("slug is human-readable, to make referencing easier"),
    )

    def __str__(self):
        return self.name

    class Meta:
        ordering = ["name"]
        verbose_name = _("Vocabulary")
        verbose_name_plural = _("Vocabularies")


class Term(models.Model):
    vocabulary = models.ForeignKey(Vocabulary, null=False, on_delete=models.CASCADE)
    vocabulary.verbose_name = _("Vocabulary")
    term = models.CharField(_("Term"), max_length=255)
    slug = models.CharField(_("Slug"), max_length=255, unique=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = self.vocabulary.slug + "__" + slugify(self.slug)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.term

    class Meta:
        ordering = ["term"]
        verbose_name = _("Term")
        verbose_name_plural = _("Terms")


class Note(models.Model):
    note = models.TextField()
    user = models.ForeignKey(
        get_user_model(), on_delete=models.SET_NULL, null=True, editable=False
    )
    created = models.DateTimeField(auto_now=True)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey("content_type", "object_id")

    def __str__(self):
        ret = f"{self.note}<br/><small><i>{(self.created or datetime.datetime.now() ).date()}"
        if self.user:
            ret += f" - {self.user}"
        ret += "</i></small>"
        return mark_safe(ret)

    class Meta:
        ordering = ["-created"]
