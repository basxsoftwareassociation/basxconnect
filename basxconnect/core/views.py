import htmlgenerator as hg
from bread import layout, menu
from bread.forms.forms import generate_form
from bread.utils.urls import aslayout, reverse, reverse_model
from bread.views import EditView
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.utils.html import mark_safe
from django.utils.translation import gettext_lazy as _
from django.views.decorators.csrf import csrf_exempt
from haystack.query import SearchQuerySet

from . import layouts
from .models import LegalPerson, NaturalPerson, Person, PersonAssociation

# ADD MODEL VIEWS AND REGISTER URLS -------------------------------------------


class NaturalPersonEditView(EditView):
    def layout(self, request):
        return layout.BaseElement(
            layouts.editperson_toolbar(request),
            layouts.editperson_head(request),
            layout.form.Form.wrap_with_form(
                layout.C("form"),
                layouts.editnaturalperson_form(request),
            ),
        )


class LegalPersonEditView(EditView):
    def layout(self, request):
        return layout.BaseElement(
            layouts.editperson_toolbar(request),
            layouts.editperson_head(request),
            layout.form.Form.wrap_with_form(
                layout.C("form"),
                layouts.editlegalperson_form(request),
            ),
        )


class PersonAssociationEditView(EditView):
    def layout(self, request):
        return layout.BaseElement(
            layouts.editperson_toolbar(request),
            layouts.editperson_head(request),
            layout.form.Form.wrap_with_form(
                layout.C("form"),
                layouts.editpersonassociation_form(request),
            ),
        )


# ADD SETTING VIEWS AND REGISTER URLS -------------------------------------------


@aslayout
def generalsettings(request):
    layoutobj = layouts.generalsettings(request)
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


@aslayout
def personsettings(request):
    return lambda request: layouts.personsettings(request)


@aslayout
def relationshipssettings(request):
    return lambda request: layouts.relationshipssettings(request)


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
def searchperson(request):
    query = request.GET.get("query")
    if not query:
        return HttpResponse("")

    objects = [
        result.object
        for result in SearchQuerySet()
        .models(NaturalPerson, LegalPerson, PersonAssociation)
        .autocomplete(name_auto=query)
        if result.object
    ]
    if not objects:
        return HttpResponse(
            hg.DIV(
                _("No results"),
                _class="bx--tile",
                style="margin-bottom: 1rem; padding: 0.5rem",
            ).render({})
        )

    return HttpResponse(
        hg.DIV(
            hg.UL(
                *[
                    hg.LI(
                        hg.DIV(
                            object,
                            hg.DIV(
                                mark_safe(
                                    object.core_postal_list.first() or _("No address")
                                ),
                                style="font-size: small; padding-bottom: 0.5rem; padding-top: 0.5rem",
                            ),
                        ),
                        style="cursor: pointer; padding: 0.5rem;",
                        onclick=(
                            "document.location = '"
                            + str(
                                reverse_model(object, "edit", kwargs={"pk": object.pk})
                            )
                            + "'"
                        ),
                        onmouseenter="this.style.backgroundColor = 'lightgray'",
                        onmouseleave="this.style.backgroundColor = 'initial'",
                    )
                    for object in objects
                ]
            ),
            _class="bx--tile",
            style="margin-bottom: 1rem; padding: 0",
        ).render({})
    )

    return HttpResponse(
        hg.DIV(
            hg.UL(
                hg.Iterator(
                    objects,
                    "person",
                    hg.LI(
                        hg.DIV(
                            hg.C("person"),
                            hg.DIV(
                                hg.F(
                                    lambda c, e: mark_safe(
                                        c["person"].core_postal_list.first()
                                        or _("No address")
                                    )
                                ),
                                style="font-size: small; padding-bottom: 1rem; padding-top: 0.5rem",
                            ),
                        ),
                        style="cursor: pointer; padding: 0.5rem;",
                        onclick=hg.BaseElement(
                            "document.location = '",
                            hg.F(lambda c, e: layout.objectaction(c["person"], "edit")),
                            "'",
                        ),
                        onmouseenter="this.style.backgroundColor = 'lightgray'",
                        onmouseleave="this.style.backgroundColor = 'initial'",
                    ),
                ),
            ),
            _class="bx--tile",
            style="margin-bottom: 2rem;",
        ).render({})
    )
