from bread import views as breadviews
from bread.utils.urls import autopath, default_model_paths, model_urlname, reverse_model
from django.views.generic import RedirectView

from basxconnect.core.views import settings_views
from basxconnect.core.views.person import (
    person_browse_views,
    person_details_views,
    person_modals_views,
    search_person_view,
)

from . import models
from .wizards.add_person import AddPersonWizard

urlpatterns = [
    autopath(
        RedirectView.as_view(
            url=reverse_model(models.Person, "addwizard", kwargs={"step": "Search"})
        ),
        model_urlname(models.Person, "add"),
    ),
    autopath(
        RedirectView.as_view(url=reverse_model(models.Person, "browse")),
        model_urlname(models.NaturalPerson, "browse"),
    ),
    autopath(
        RedirectView.as_view(url=reverse_model(models.Person, "browse")),
        model_urlname(models.LegalPerson, "browse"),
    ),
    autopath(
        RedirectView.as_view(url=reverse_model(models.Person, "browse")),
        model_urlname(models.PersonAssociation, "browse"),
    ),
    autopath(
        AddPersonWizard.as_view(url_name=model_urlname(models.Person, "addwizard")),
        model_urlname(models.Person, "addwizard"),
    ),
    *default_model_paths(
        models.Person,
        browseview=person_browse_views.PersonBrowseView,
        deleteview=breadviews.DeleteView._with(softdeletefield="deleted"),
    ),
    *default_model_paths(
        models.NaturalPerson,
        editview=person_details_views.NaturalPersonEditView,
        readview=person_details_views.NaturalPersonReadView,
        deleteview=breadviews.DeleteView._with(softdeletefield="deleted"),
        copyview=breadviews.generate_copyview(
            models.NaturalPerson,
            attrs={
                "personnumber": models.random_personid,
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
        editview=person_details_views.LegalPersonEditView,
        readview=person_details_views.LegalPersonReadView,
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
        editview=person_details_views.PersonAssociationEditView,
        readview=person_details_views.PersonAssociationReadView,
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
    autopath(settings_views.generalsettings),
    autopath(
        person_details_views.togglepersonstatus,
        model_urlname(models.Person, "togglestatus"),
    ),
    autopath(settings_views.personsettings),
    autopath(settings_views.relationshipssettings),
    autopath(search_person_view.searchperson),
    autopath(
        person_modals_views.NaturalPersonEditMailingsView.as_view(
            model=models.NaturalPerson
        )
    ),
    autopath(
        person_modals_views.LegalPersonEditMailingsView.as_view(
            model=models.LegalPerson
        )
    ),
    autopath(
        person_modals_views.NaturalPersonEditPersonalDataView.as_view(
            model=models.NaturalPerson
        )
    ),
    autopath(
        person_modals_views.LegalPersonEditPersonalDataView.as_view(
            model=models.LegalPerson
        )
    ),
    autopath(
        person_modals_views.PersonAssociationEditPersonalDataView.as_view(
            model=models.PersonAssociation
        )
    ),
    autopath(person_modals_views.EditPostalAddressView.as_view(model=models.Postal)),
    autopath(person_modals_views.AddPostalAddressView.as_view(model=models.Postal)),
]
