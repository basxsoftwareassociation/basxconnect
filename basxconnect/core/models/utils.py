import datetime

from django.contrib.auth import get_user_model
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.utils.html import mark_safe
from django.utils.translation import gettext_lazy as _


class Category(models.Model):
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
        verbose_name = _("Category")
        verbose_name_plural = _("Categories")


class Term(models.Model):
    category = models.ForeignKey(Category, null=False, on_delete=models.CASCADE)
    category.verbose_name = _("Category")
    term = models.CharField(_("Term"), max_length=255)

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
