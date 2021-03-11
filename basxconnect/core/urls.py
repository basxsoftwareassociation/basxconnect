import htmlgenerator as hg
from bread import views as breadviews
from bread.menu import Link
from bread.utils.urls import (
    default_model_paths,
    generate_path,
    model_urlname,
    reverse,
    reverse_model,
)
from django.utils.translation import gettext_lazy as _
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
        browseview=breadviews.BrowseView._with(
            columns=[
                "personnumber",
                "status",
                (_("Category"), hg.C("row._type"), "_type"),
                "name",
                "primary_postal_address.address",
                "primary_postal_address.postcode",
                "primary_postal_address.city",
                "primary_postal_address.country",
                (
                    _("Email"),
                    hg.C(
                        "row.primary_email_address.asbutton",
                    ),
                    "primary_email_address__email",
                    False,
                ),
            ],
            bulkactions=(
                Link(
                    reverse_model(models.Person, "bulkdelete"),
                    label=_("Delete"),
                    icon="trash-can",
                ),
                Link(
                    reverse_model(models.Person, "export"),
                    label="Excel",
                    icon="download",
                ),
            ),
            searchurl=reverse("basxconnect.core.views.searchperson"),
            rowclickaction="read",
            filteroptions=[
                (
                    models.NaturalPerson._meta.verbose_name_plural,
                    '_maintype = "naturalperson"',
                ),
                (
                    models.LegalPerson._meta.verbose_name_plural,
                    '_maintype = "legalperson"',
                ),
                (
                    models.PersonAssociation._meta.verbose_name_plural,
                    '_maintype = "personassociation"',
                ),
            ],
        ),
    ),
    generate_path(
        breadviews.generate_excel_view(
            models.Person.objects.all(),
            [
                "personnumber",
                "status",
                "maintype",
                "name",
                "address",
                "postalcode",
                "city",
                "country",
            ],
        ),
        model_urlname(models.Person, "export"),
    ),
    *default_model_paths(
        models.NaturalPerson,
        editview=views.NaturalPersonEditView,
        readview=views.NaturalPersonReadView,
        copyview=breadviews.generate_copyview(
            models.NaturalPerson, attrs={"personnumber": None}, labelfield="name"
        ),
    ),
    *default_model_paths(
        models.LegalPerson,
        editview=views.LegalPersonEditView,
        readview=views.LegalPersonReadView,
    ),
    *default_model_paths(
        models.PersonAssociation,
        editview=views.PersonAssociationEditView,
        readview=views.PersonAssociationReadView,
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
        breadviews.BulkDeleteView.as_view(model=models.Person),
        model_urlname(models.Person, "bulkdelete"),
    ),
]
