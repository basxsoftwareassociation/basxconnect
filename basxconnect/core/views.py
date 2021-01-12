import htmlgenerator as hg
from bread import layout, menu
from bread.forms.forms import generate_form
from bread.utils.urls import (
    aslayout,
    model_urlname,
    registermodelurl,
    registerurl,
    reverse,
    reverse_model,
)
from bread.views import (
    BrowseView,
    EditView,
    generate_copyview,
    register_default_modelviews,
)
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.utils.html import mark_safe
from django.utils.translation import gettext_lazy as _
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import RedirectView
from haystack.query import SearchQuerySet

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
)


class NaturalPersonEditView(EditView):
    def layout(self, request):
        return layout.ObjectContext(
            self.object,
            layout.BaseElement(
                layout.get_layout("basxconnect.core.layouts.editperson_toolbar")(),
                layout.get_layout("basxconnect.core.layouts.editperson_head")(),
                layout.form.Form.wrap_with_form(
                    layout.C("form"),
                    layout.get_layout(
                        "basxconnect.core.layouts.editnaturalperson_form"
                    )(),
                ),
            ),
        )


class LegalPersonEditView(EditView):
    def layout(self, request):
        return layout.ObjectContext(
            self.object,
            layout.BaseElement(
                layout.get_layout("basxconnect.core.layouts.editperson_toolbar")(),
                layout.get_layout("basxconnect.core.layouts.editperson_head")(),
                layout.form.Form.wrap_with_form(
                    layout.C("form"),
                    layout.get_layout(
                        "basxconnect.core.layouts.editlegalperson_form"
                    )(),
                ),
            ),
        )


class PersonAssociationEditView(EditView):
    def layout(self, request):
        return layout.ObjectContext(
            self.object,
            layout.BaseElement(
                layout.get_layout("basxconnect.core.layouts.editperson_toolbar")(),
                layout.get_layout("basxconnect.core.layouts.editperson_head")(),
                layout.form.Form.wrap_with_form(
                    layout.C("form"),
                    layout.get_layout(
                        "basxconnect.core.layouts.editpersonassociation_form"
                    )(),
                ),
            ),
        )


register_default_modelviews(
    NaturalPerson,
    editview=NaturalPersonEditView,
    copyview=generate_copyview(
        NaturalPerson, attrs={"personnumber": None}, labelfield="name"
    ),
)
register_default_modelviews(LegalPerson, editview=LegalPersonEditView)

register_default_modelviews(
    PersonAssociation, editview=PersonAssociationEditView
)  # uses AddPersonWizard
register_default_modelviews(RelationshipType)
register_default_modelviews(Relationship)
register_default_modelviews(Term)
register_default_modelviews(Category)


# ADD SETTING VIEWS AND REGISTER URLS -------------------------------------------


@registerurl
@aslayout
def generalsettings(request):
    layoutobj = layout.get_layout("basxconnect.core.layouts.generalsettings")()
    form = generate_form(
        request,
        LegalPerson,
        layoutobj,
        LegalPerson.objects.get(id=1),  # must exists due to migration
    )

    if request.method == "POST":
        if form.is_valid():
            form.save()

    return lambda request: hg.BaseElement(
        hg.H3(_("General")),
        hg.H4(_("Information about our organization")),
        layout.form.Form(form, layoutobj),
    )


@csrf_exempt
def togglepersonstatus(request, pk: int):
    if request.method == "POST":
        person = get_object_or_404(Person, pk=pk)
        person.active = not person.active
        person.save()
    return HttpResponse(
        _("%s is %s") % (person, _("Active") if person.active else _("Inactive"))
    )


registermodelurl(Person, "togglestatus", togglepersonstatus)


@registerurl
@aslayout
def personsettings(request):
    return lambda request: layout.get_layout(
        "basxconnect.core.layouts.personsettings"
    )()


@registerurl
@aslayout
def relationshipssettings(request):
    return lambda request: layout.get_layout(
        "basxconnect.core.layouts.relationshipssettings"
    )()


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
        menu.Link(reverse("basxconnect.core.views.personsettings"), _("Persons")),
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

    objects = [
        result.object
        for result in SearchQuerySet()
        .models(NaturalPerson, LegalPerson, PersonAssociation)
        .autocomplete(name_auto=query)
    ]

    return HttpResponse(
        hg.DIV(
            hg.UL(
                hg.Iterator(
                    objects,
                    hg.LI(
                        layout.ObjectContext.Binding(hg.DIV)(
                            layout.ObjectLabel(),
                            layout.ObjectContext.Binding(hg.DIV)(
                                hg.F(
                                    lambda c, e: mark_safe(
                                        e.object.core_postal_list.first()
                                        or _("No address")
                                    )
                                ),
                                style="font-size: small; padding-bottom: 1rem; padding-top: 0.5rem",
                            ),
                        ),
                        style="cursor: pointer; padding: 0.5rem;",
                        onclick=hg.BaseElement(
                            "document.location = '", layout.ObjectAction("edit"), "'"
                        ),
                        onmouseenter="this.style.backgroundColor = 'lightgray'",
                        onmouseleave="this.style.backgroundColor = 'initial'",
                    ),
                    layout.ObjectContext,
                ),
            ),
            _class="bx--tile",
            style="margin-bottom: 2rem;",
        ).render({})
    )
