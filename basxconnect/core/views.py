import htmlgenerator as hg
from bread import layout as _layout
from bread import menu
from bread.forms.forms import generate_form
from bread.menu import Action, Link
from bread.utils.urls import aslayout, reverse, reverse_model
from bread.views import BrowseView, EditView, ReadView, layoutasreadonly
from django import forms
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.utils.html import mark_safe
from django.utils.translation import gettext_lazy as _
from django.views.decorators.csrf import csrf_exempt
from haystack.query import SearchQuerySet

from . import layouts, models, settings

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
        Action(
            js="var u = new window.URL(window.location.toString()); u.search += '&export=1'; window.location = u.toString()",
            label="Excel",
            icon="download",
        ),
    )
    searchurl = reverse("basxconnect.core.views.searchperson")
    rowclickaction = "read"

    class FilterForm(forms.Form):
        naturalperson = forms.BooleanField(required=False, label=_("Natural Person"))
        legalperson = forms.BooleanField(required=False, label=_("Legal Person"))
        personassociation = forms.BooleanField(
            required=False, label=_("Person Association")
        )
        naturalperson_subtypes = forms.ModelMultipleChoiceField(
            queryset=models.Term.objects.filter(category__slug="naturaltype"),
            widget=forms.CheckboxSelectMultiple,
            required=False,
        )
        legalperson_subtypes = forms.ModelMultipleChoiceField(
            queryset=models.Term.objects.filter(category__slug="legaltype"),
            widget=forms.CheckboxSelectMultiple,
            required=False,
        )
        personassociation_subtypes = forms.ModelMultipleChoiceField(
            queryset=models.Term.objects.filter(category__slug="associationtype"),
            widget=forms.CheckboxSelectMultiple,
            required=False,
        )
        categories = forms.ModelMultipleChoiceField(
            queryset=models.Term.objects.filter(category__slug="category"),
            widget=forms.CheckboxSelectMultiple,
            required=False,
        )
        preferred_language = forms.MultipleChoiceField(
            choices=settings.PREFERRED_LANGUAGES,
            widget=forms.CheckboxSelectMultiple,
            required=False,
        )
        status = forms.MultipleChoiceField(
            choices=[("active", _("Active")), ("inactive", _("Inactive"))],
            widget=forms.CheckboxSelectMultiple,
            required=False,
        )

    def _filterform(self):
        return self.FilterForm({"status": ["active"], **self.request.GET})

    def get_queryset(self):
        ret = super().get_queryset()
        form = self._filterform()
        if form.is_valid():
            if any(
                [
                    form.cleaned_data[i]
                    for i in (
                        "naturalperson",
                        "legalperson",
                        "personassociation",
                        "naturalperson_subtypes",
                        "legalperson_subtypes",
                        "personassociation_subtypes",
                    )
                ]
            ):
                q = Q()
                for i in ("naturalperson", "legalperson", "personassociation"):
                    if form.cleaned_data[i]:
                        q |= Q(_maintype=i)
                    if form.cleaned_data[f"{i}_subtypes"]:
                        q |= Q(_type__in=form.cleaned_data[f"{i}_subtypes"])
                ret = ret.filter(q)
            if form.cleaned_data.get("categories"):
                ret = ret.filter(categories__in=form.cleaned_data["categories"])
            if form.cleaned_data.get("preferred_language"):
                ret = ret.filter(
                    preferred_language__in=form.cleaned_data["preferred_language"]
                )
            if len(form.cleaned_data.get("status")) == 1:
                ret = ret.filter(active=form.cleaned_data.get("status")[0] == "active")

        return ret

    def get_settingspanel(self):
        return hg.DIV(
            _layout.form.Form(
                self._filterform(),
                hg.DIV(
                    hg.DIV(
                        hg.DIV(_layout.helpers.Label(_("Categories"))),
                        hg.DIV(
                            hg.DIV(
                                hg.DIV(
                                    _layout.form.FormField(
                                        "naturalperson",
                                        elementattributes={
                                            "onclick": "updateCheckboxGroupItems(this.parentElement.parentElement)"
                                        },
                                    ),
                                    hg.DIV(
                                        _layout.form.FormField(
                                            "naturalperson_subtypes",
                                            elementattributes={
                                                "style": "padding-left: 1rem",
                                            },
                                        ),
                                        style="margin-top: -2rem; margin-bottom: 1rem",
                                    ),
                                ),
                                _layout.form.FormField(
                                    "personassociation",
                                    elementattributes={
                                        "onclick": "updateCheckboxGroupItems(this.parentElement.parentElement)"
                                    },
                                ),
                                hg.DIV(
                                    _layout.form.FormField(
                                        "personassociation_subtypes",
                                        elementattributes={
                                            "style": "padding-left: 1rem"
                                        },
                                    ),
                                    style="margin-top: -2rem; margin-bottom: 1rem",
                                ),
                                style="margin-right: 1rem",
                            ),
                            hg.DIV(
                                _layout.form.FormField(
                                    "legalperson",
                                    elementattributes={
                                        "onclick": "updateCheckboxGroupItems(this.parentElement.parentElement)"
                                    },
                                ),
                                hg.DIV(
                                    _layout.form.FormField(
                                        "legalperson_subtypes",
                                        elementattributes={
                                            "style": "padding-left: 1rem"
                                        },
                                    ),
                                    style="margin-top: -2rem; margin-bottom: 1rem",
                                ),
                                style="margin-right: 1rem",
                            ),
                            style="display: flex",
                        ),
                        style="border-right: #ccc solid 1px; margin-top: 1rem",
                        _class="bx--tile",
                    ),
                    hg.DIV(
                        hg.DIV(_layout.helpers.Label(_("Tags"))),
                        _layout.form.FormField("categories"),
                        style="border-right: #ccc solid 1px; margin-top: 1rem; overflow-y: scroll",
                        _class="bx--tile",
                    ),
                    hg.DIV(
                        hg.DIV(_layout.helpers.Label(_("Languages"))),
                        _layout.form.FormField("preferred_language"),
                        style="border-right: #ccc solid 1px; margin-top: 1rem",
                        _class="bx--tile",
                    ),
                    hg.DIV(
                        hg.DIV(_layout.helpers.Label(_("Status"))),
                        _layout.form.FormField("status"),
                        style="margin-top: 1rem",
                        _class="bx--tile",
                    ),
                    style="display: flex; margin: -1rem; padding-bottom: 2rem; max-height: 50vh",
                ),
                hg.DIV(
                    _layout.button.Button(
                        ("Filter"),
                        type="submit",
                        style="float: right",
                    ),
                    _layout.button.Button(
                        ("Reset"),
                        buttontype="secondary",
                        style="float: right",
                        islink=True,
                        href=self.request.path,
                    ),
                    _layout.button.Button(
                        ("Cancel"),
                        buttontype="ghost",
                        style="float: right",
                        onclick="this.parentElement.parentElement.parentElement.parentElement.parentElement.style.display = 'none'",
                    ),
                    style="margin-bottom: 2rem; margin-right: -1rem",
                ),
                method="GET",
            ),
            hg.SCRIPT(
                mark_safe(
                    """
                    function updateCheckboxGroupItems(group) {
                        var items = $$('input[type=checkbox]', group);
                        var value = items[0].getAttribute('aria-checked');
                        value = value == 'true' ? 'true' : 'false';
                        for(var i = 1; i < items.length; ++i) {
                            new CarbonComponents.Checkbox(items[i]).setState(value);
                        }
                    }
                    """
                )
            ),
        )


# ADD SETTING VIEWS AND REGISTER URLS -------------------------------------------


@aslayout
def generalsettings(request):
    layoutobj = layouts.generalsettings(request)
    form = generate_form(
        request,
        models.LegalPerson,
        layoutobj,
        models.Person.objects.get(id=settings.OWNER_PERSON_ID),
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
        person = get_object_or_404(models.Person, pk=pk)
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
    menu.Item(
        menu.Link(reverse_model(models.Person, "browse"), _("Persons")), persongroup
    )
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
        .models(models.NaturalPerson, models.LegalPerson, models.PersonAssociation)
        .autocomplete(name_auto=query)
        if result.object
    ]
    if not objects:
        return HttpResponse(
            hg.DIV(
                _("No results"),
                _class="bx--tile raised",
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
            _class="bx--tile raised",
        ).render({})
    )
