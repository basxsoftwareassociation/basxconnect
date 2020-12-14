import htmlgenerator as hg
from bread import layout, menu
from bread.forms.forms import generate_form
from bread.utils.urls import (
    aslayout,
    model_urlname,
    registerurl,
    reverse,
    reverse_model,
)
from bread.views import BrowseView, EditView, register_default_modelviews
from django.http import HttpResponse
from django.utils.html import mark_safe
from django.utils.translation import gettext_lazy as _
from django.views.generic import RedirectView
from haystack.query import SearchQuerySet

from .layouts import Layouts
from .models import (
    Category,
    LegalPerson,
    NaturalPerson,
    Person,
    PersonAssociation,
    Relationship,
    RelationshipType,
    Term,
)
from .wizards.add_person import AddPersonWizard

# ADD MODEL VIEWS AND REGISTER URLS -------------------------------------------

# add url for person needs a redirect to the wizard
# specifying the wizardview direclty is problematic
# All person "add" views should go through the wizard and are therefore not registered
registerurl(model_urlname(Person, "add"))(
    RedirectView.as_view(
        url=reverse_model(Person, "addwizard", kwargs={"step": "Search"})
    )
)
registerurl(model_urlname(NaturalPerson, "browse"))(
    RedirectView.as_view(url=reverse_model(Person, "browse"))
)
registerurl(model_urlname(LegalPerson, "browse"))(
    RedirectView.as_view(url=reverse_model(Person, "browse"))
)
registerurl(model_urlname(PersonAssociation, "browse"))(
    RedirectView.as_view(url=reverse_model(Person, "browse"))
)
registerurl(model_urlname(Person, "addwizard"))(
    AddPersonWizard.as_view(url_name=model_urlname(Person, "addwizard"))
)
register_default_modelviews(
    Person,
    browseview=BrowseView._with(
        fields=[
            "number",
            "status",
            "type",
            "name",
            "street",
            "postalcode",
            "city",
            "country",
        ],
    ),
)
register_default_modelviews(
    NaturalPerson,
    editview=EditView._with(
        formlayout=lambda _self, request: Layouts.person_edit_layout
    ),  # use lambda for late evaluation of the layout
)

register_default_modelviews(LegalPerson)  # uses AddPersonWizard
register_default_modelviews(PersonAssociation)  # uses AddPersonWizard
register_default_modelviews(RelationshipType)
register_default_modelviews(Relationship)
register_default_modelviews(Term)
register_default_modelviews(Category)


# ADD SETTING VIEWS AND REGISTER URLS -------------------------------------------


@registerurl
@aslayout
def generalsettings(request):
    instance = LegalPerson.objects.get(id=1)  # must exists due to migration
    form = generate_form(request, LegalPerson, Layouts.generalsettings_layout, instance)

    if request.method == "POST":
        if form.is_valid():
            form.save()

    return lambda request: hg.BaseElement(
        hg.H1(_("General")),
        hg.H2(_("Information about our organization")),
        layout.form.Form(form, Layouts.generalsettings_layout),
    )


@registerurl
@aslayout
def appearancesettings(request):
    return lambda request: Layouts.appearancesettings_layout


@registerurl
@aslayout
def personssettings(request):
    return lambda request: Layouts.personssettings_layout


@registerurl
@aslayout
def relationshipssettings(request):
    return lambda request: Layouts.relationshipssettings_layout


@registerurl
@aslayout
def apikeyssettings(request):
    return lambda request: Layouts.apikeyssettings_layout


# MENU ENTRIES ---------------------------------------------------------------------

settingsgroup = menu.Group(_("Settings"), icon="settings")
persongroup = menu.Group(_("Persons"), icon="group")

menu.registeritem(
    menu.Item(menu.Link(reverse_model(Person, "browse"), _("Persons")), persongroup)
)

menu.registeritem(
    menu.Item(
        menu.Link(reverse("basxconnect.core.views.generalsettings"), _("General")),
        settingsgroup,
    )
)
menu.registeritem(
    menu.Item(
        menu.Link(reverse("basxconnect.core.views.personssettings"), _("Persons")),
        settingsgroup,
    )
)
menu.registeritem(
    menu.Item(
        menu.Link(
            reverse("basxconnect.core.views.relationshipssettings"),
            _("Relationships"),
        ),
        settingsgroup,
    )
)


# Search view
# simple person search view, for use with ajax calls
@registerurl
def searchperson(request):
    query = request.GET.get("query")
    if not query:
        return HttpResponse("")

    qs = (
        SearchQuerySet()
        .models(NaturalPerson, LegalPerson, PersonAssociation)
        .autocomplete(name_auto=query)
    )
    items = [
        hg.LI(
            result.object,
            hg.DIV(
                mark_safe(result.object.core_postal_list.first() or _("No address")),
                style="font-size: small; margin-bottom: 1rem;",
            ),
        )
        for result in qs
    ]

    return HttpResponse(
        hg.UL(
            *(items or [hg.LI(_("No results"))]),
            _class="bx--tile",
            style="margin-bottom: 2rem;"
        ).render({})
    )
