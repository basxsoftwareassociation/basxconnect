import htmlgenerator as hg
from bread import layout as _layout
from bread import menu
from bread.forms.forms import generate_form
from bread.menu import Link
from bread.utils.urls import aslayout, reverse, reverse_model
from bread.views import BrowseView, EditView, ReadView, layoutasreadonly
from django import forms
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.utils.html import mark_safe
from django.utils.translation import gettext_lazy as _
from django.views.decorators.csrf import csrf_exempt
from haystack.query import SearchQuerySet

from . import layouts, models, settings
from .models import LegalPerson, NaturalPerson, Person, PersonAssociation

# ADD MODEL VIEWS AND REGISTER URLS -------------------------------------------


def personform_shortcut(request, formlayout, isreadview):
    return hg.BaseElement(
        layouts.editperson_toolbar(request),
        layouts.editperson_head(request, isreadview=isreadview),
        _layout.form.Form(hg.C("form"), formlayout),
    )


class NaturalPersonEditView(EditView):
    def layout(self, request):
        return personform_shortcut(
            request, layouts.editnaturalperson_form(request), isreadview=False
        )


class NaturalPersonReadView(ReadView):
    def layout(self, request):
        return layoutasreadonly(
            personform_shortcut(
                request, layouts.editnaturalperson_form(request), isreadview=True
            )
        )


class LegalPersonEditView(EditView):
    def layout(self, request):
        return personform_shortcut(
            request, layouts.editlegalperson_form(request), isreadview=False
        )


class LegalPersonReadView(ReadView):
    def layout(self, request):
        return layoutasreadonly(
            personform_shortcut(
                request, layouts.editlegalperson_form(request), isreadview=True
            )
        )


class PersonAssociationEditView(EditView):
    def layout(self, request):
        return personform_shortcut(
            request, layouts.editpersonassociation_form(request), isreadview=False
        )


class PersonAssociationReadView(ReadView):
    def layout(self, request):
        return layoutasreadonly(
            personform_shortcut(
                request, layouts.editpersonassociation_form(request), isreadview=True
            )
        )


class PersonBrowseView(BrowseView):
    columns = [
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
    ]
    bulkactions = (
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
    )
    searchurl = reverse("basxconnect.core.views.searchperson")
    rowclickaction = "read"
    filteroptions = [
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
    ]

    class FilterForm(forms.Form):
        show_inactive = forms.BooleanField(required=False, label=_("Show inactive"))
        preferred_language = forms.ChoiceField(
            choices=[(None, "--------")] + settings.PREFERRED_LANGUAGES,
            required=False,
            label=_("Preferred Language"),
        )
        _type = forms.ModelMultipleChoiceField(
            queryset=models.Term.objects.filter(
                category__slug__in=["naturaltype", "legaltype", "associationtype"]
            ),
            required=False,
            label=_("Person Category"),
        )
        categories = forms.ModelMultipleChoiceField(
            queryset=models.Term.objects.filter(category__slug="category"),
            required=False,
            label=_("Categories"),
        )

    def get_queryset(self, *args, **kwargs):
        qs = super().get_queryset(*args, **kwargs)
        form = self.FilterForm(self.request.GET)
        if form.is_valid():
            for field in form.fields.keys():
                if field in form.cleaned_data and not form.cleaned_data[field]:
                    form.cleaned_data.pop(field)
            if not form.cleaned_data.pop("show_inactive", False):
                form.cleaned_data["active"] = True
            if "_type" in form.cleaned_data:
                form.cleaned_data["_type__in"] = form.cleaned_data.pop("_type")
            if "categories" in form.cleaned_data:
                form.cleaned_data["categories__in"] = form.cleaned_data.pop(
                    "categories"
                )
            qs = qs.filter(**form.cleaned_data)
        return qs

    def layout(self, *args, **kwargs):
        form = self.FilterForm(self.request.GET)
        ret = super().layout(*args, **kwargs)
        filters = _layout.form.Form(
            form,
            _layout.grid.Grid(
                _layout.grid.Row(
                    _layout.grid.Col(
                        _layout.form.FormField("show_inactive"),
                        width=2,
                        breakpoint="lg",
                    ),
                    _layout.grid.Col(
                        _layout.form.FormField("preferred_language"),
                        width=3,
                        breakpoint="lg",
                    ),
                    _layout.grid.Col(
                        _layout.form.FormField("_type"),
                        width=4,
                        breakpoint="lg",
                    ),
                    _layout.grid.Col(
                        _layout.form.FormField("categories"),
                        width=4,
                        breakpoint="lg",
                    ),
                    _layout.grid.Col(
                        _layout.button.Button(
                            icon="filter--remove",
                            onclick=f"window.location = '{self.request.path}'",
                            buttontype="secondary",
                            style="margin-left: 0.25rem; float: right",
                        ),
                        _layout.button.Button(
                            "Filter",
                            icon="filter",
                            type="submit",
                            style="float: right",
                        ),
                        width=3,
                        breakpoint="lg",
                    ),
                )
            ),
            method="GET",
        )
        ret[0].append(filters)
        return ret


# ADD SETTING VIEWS AND REGISTER URLS -------------------------------------------


@aslayout
def generalsettings(request):
    layoutobj = layouts.generalsettings(request)
    form = generate_form(
        request,
        LegalPerson,
        layoutobj,
        Person.objects.get(id=settings.OWNER_PERSON_ID),
    )

    if request.method == "POST":
        if form.is_valid():
            form.save()

    return lambda request: hg.BaseElement(
        hg.H3(_("General")),
        hg.H4(_("Information about our organization")),
        _layout.form.Form(form, layoutobj),
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

persongroup = menu.Group(_("Persons"), icon="group")
settingsgroup = menu.Group(_("Settings"), icon="settings", order=100)

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
    query = request.GET.get("q")
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
                style="margin-bottom: 1rem; padding: 0.5rem; opacity: 0.85; outline: auto",
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
            style="margin-bottom: 1rem; padding: 0; opacity: 0.95; outline: auto",
        ).render({})
    )
