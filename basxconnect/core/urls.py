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

x = breadviews.BrowseView._with(
    fields=[
        "personnumber",
        "status",
        "type",
        "name",
        "address",
        "postalcode",
        "city",
        "country",
    ]
)
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
        browseview=breadviews.BrowseView._with(
            fields=[
                "personnumber",
                "status",
                "type",
                "name",
                "address",
                "postalcode",
                "city",
                "country",
            ],
        ),
    ),
    *default_model_paths(
        models.NaturalPerson,
        editview=views.NaturalPersonEditView,
        copyview=breadviews.generate_copyview(
            models.NaturalPerson, attrs={"personnumber": None}, labelfield="name"
        ),
    ),
    *default_model_paths(models.LegalPerson, editview=views.LegalPersonEditView),
    *default_model_paths(
        models.PersonAssociation, editview=views.PersonAssociationEditView
    ),
    *default_model_paths(models.RelationshipType),
    *default_model_paths(models.Term),
    *default_model_paths(models.Category),
    generate_path(views.generalsettings),
    generate_path(views.generalsettings),
    generate_path(
        views.togglepersonstatus, model_urlname(models.Person, "togglestatus")
    ),
    generate_path(views.personsettings),
    generate_path(views.relationshipssettings),
    generate_path(views.searchperson),
]
