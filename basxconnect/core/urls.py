from bread import views as breadviews
from bread.utils.urls import (
    default_model_paths,
    generate_path,
    model_urlname,
    reverse_model,
)
from django.views.generic import RedirectView

from . import models, views
from .wizards.add_person import AddPersonWizard

urlpatterns = [
    generate_path(
        RedirectView.as_view(
            url=reverse_model(models.Person, "addwizard", kwargs={"step": "Search"})
        ),
        model_urlname(models.Person, "add"),
    ),
    generate_path(
        RedirectView.as_view(url=reverse_model(models.Person, "browse")),
        model_urlname(models.NaturalPerson, "browse"),
    ),
    generate_path(
        RedirectView.as_view(url=reverse_model(models.Person, "browse")),
        model_urlname(models.LegalPerson, "browse"),
    ),
    generate_path(
        RedirectView.as_view(url=reverse_model(models.Person, "browse")),
        model_urlname(models.PersonAssociation, "browse"),
    ),
    generate_path(
        AddPersonWizard.as_view(url_name=model_urlname(models.Person, "addwizard")),
        model_urlname(models.Person, "addwizard"),
    ),
    *default_model_paths(
        models.Person,
        browseview=views.PersonBrowseView,
        deleteview=breadviews.DeleteView._with(softdeletefield="deleted"),
    ),
    *default_model_paths(
        models.NaturalPerson,
        editview=views.NaturalPersonEditView,
        readview=views.NaturalPersonReadView,
        deleteview=breadviews.DeleteView._with(softdeletefield="deleted"),
        copyview=breadviews.generate_copyview(
            models.NaturalPerson,
            attrs={
                "personnumber": None,
                "primary_postal_address": None,
                "primary_email_address": None,
            },
            labelfield="name",
            copy_related_fields=(
                "core_web_list",
                "core_email_list",
                "core_phone_list",
                "core_fax_list",
                "core_postal_list",
            ),
        ),
    ),
    *default_model_paths(
        models.LegalPerson,
        editview=views.LegalPersonEditView,
        readview=views.LegalPersonReadView,
        deleteview=breadviews.DeleteView._with(softdeletefield="deleted"),
        copyview=breadviews.generate_copyview(
            models.LegalPerson,
            attrs={
                "personnumber": None,
                "primary_postal_address": None,
                "primary_email_address": None,
            },
            labelfield="name",
            copy_related_fields=(
                "core_web_list",
                "core_email_list",
                "core_phone_list",
                "core_fax_list",
                "core_postal_list",
            ),
        ),
    ),
    *default_model_paths(
        models.PersonAssociation,
        editview=views.PersonAssociationEditView,
        readview=views.PersonAssociationReadView,
        deleteview=breadviews.DeleteView._with(softdeletefield="deleted"),
        copyview=breadviews.generate_copyview(
            models.PersonAssociation,
            attrs={
                "personnumber": None,
                "primary_postal_address": None,
                "primary_email_address": None,
            },
            labelfield="name",
            copy_related_fields=(
                "core_web_list",
                "core_email_list",
                "core_phone_list",
                "core_fax_list",
                "core_postal_list",
            ),
        ),
    ),
    *default_model_paths(models.Relationship),
    *default_model_paths(models.RelationshipType),
    *default_model_paths(models.Term),
    *default_model_paths(models.Category),
    generate_path(views.generalsettings),
    generate_path(
        views.togglepersonstatus, model_urlname(models.Person, "togglestatus")
    ),
    generate_path(views.personsettings),
    generate_path(views.relationshipssettings),
    generate_path(views.searchperson),
    generate_path(
        breadviews.BulkDeleteView.as_view(
            model=models.Person, softdeletefield="deleted"
        ),
        model_urlname(models.Person, "bulkdelete"),
    ),
]
