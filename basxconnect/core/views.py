import htmlgenerator as hg
from bread import layout as layout
from bread import menu
from bread.forms.forms import generate_form
from bread.menu import Link
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
from haystack.utils.highlighting import Highlighter

from . import layouts, models, settings

# ADD MODEL VIEWS AND REGISTER URLS -------------------------------------------


def personform_shortcut(request, formlayout, isreadview):
    return hg.BaseElement(
        layouts.editperson_toolbar(request),
        layouts.editperson_head(request, isreadview=isreadview),
        layout.form.Form(hg.C("form"), formlayout),
    )


class NaturalPersonEditView(EditView):
    def layout(self):
        return personform_shortcut(
            self.request,
            layouts.editnaturalperson_form(self.request),
            isreadview=False,
        )


class NaturalPersonReadView(ReadView):
    def layout(self):
        return layoutasreadonly(
            personform_shortcut(
                self.request,
                layouts.editnaturalperson_form(self.request),
                isreadview=True,
            )
        )


class LegalPersonEditView(EditView):
    def layout(self):
        return personform_shortcut(
            self.request,
            layouts.editlegalperson_form(self.request),
            isreadview=False,
        )


class LegalPersonReadView(ReadView):
    def layout(self):
        return layoutasreadonly(
            personform_shortcut(
                self.request,
                layouts.editlegalperson_form(self.request),
                isreadview=True,
            )
        )


class PersonAssociationEditView(EditView):
    def layout(self):
        return personform_shortcut(
            self.request,
            layouts.editpersonassociation_form(self.request),
            isreadview=False,
        )


class PersonAssociationReadView(ReadView):
    def layout(self):
        return layoutasreadonly(
            personform_shortcut(
                self.request,
                layouts.editpersonassociation_form(self.request),
                isreadview=True,
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
            reverse_model(models.Person, "excel"),
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
            layout.form.Form(
                self._filterform(),
                hg.DIV(
                    hg.DIV(
                        hg.DIV(layout.helpers.Label(_("Categories"))),
                        hg.DIV(
                            hg.DIV(
                                hg.DIV(
                                    layout.form.FormField(
                                        "naturalperson",
                                        elementattributes={
                                            "onclick": "updateCheckboxGroupItems(this.parentElement.parentElement)"
                                        },
                                    ),
                                    hg.DIV(
                                        layout.form.FormField(
                                            "naturalperson_subtypes",
                                            elementattributes={
                                                "style": "padding-left: 1rem",
                                            },
                                        ),
                                        style="",
                                    ),
                                ),
                                layout.form.FormField(
                                    "personassociation",
                                    elementattributes={
                                        "onclick": "updateCheckboxGroupItems(this.parentElement.parentElement)"
                                    },
                                ),
                                hg.DIV(
                                    layout.form.FormField(
                                        "personassociation_subtypes",
                                        elementattributes={
                                            "style": "padding-left: 1rem"
                                        },
                                    ),
                                    style="",
                                ),
                                style="margin-right: 16px",
                            ),
                            hg.DIV(
                                layout.form.FormField(
                                    "legalperson",
                                    elementattributes={
                                        "onclick": "updateCheckboxGroupItems(this.parentElement.parentElement)"
                                    },
                                ),
                                hg.DIV(
                                    layout.form.FormField(
                                        "legalperson_subtypes",
                                        elementattributes={
                                            "style": "padding-left: 1rem"
                                        },
                                    ),
                                    style="",
                                ),
                                style="margin-right: 16px",
                            ),
                            style="display: flex",
                        ),
                        style="border-right: #ccc solid 1px; margin: 0 16px 0 0",
                    ),
                    hg.DIV(
                        hg.DIV(layout.helpers.Label(_("Tags"))),
                        hg.DIV(
                            layout.form.FormField("categories"),
                            style="margin-right: 16px",
                        ),
                        style="border-right: #ccc solid 1px; margin: 0 16px 0 0; overflow-y: scroll",
                    ),
                    hg.DIV(
                        hg.DIV(layout.helpers.Label(_("Languages"))),
                        hg.DIV(
                            layout.form.FormField("preferred_language"),
                            style="margin-right: 16px",
                        ),
                        style="border-right: #ccc solid 1px; margin: 0 16px 0 0",
                    ),
                    hg.DIV(
                        hg.DIV(layout.helpers.Label(_("Status"))),
                        layout.form.FormField("status"),
                    ),
                    style="display: flex; max-height: 50vh; padding: 24px 32px 0 32px",
                ),
                hg.DIV(
                    layout.button.Button(
                        ("Cancel"),
                        buttontype="ghost",
                        onclick="this.parentElement.parentElement.parentElement.parentElement.parentElement.style.display = 'none'",
                    ),
                    layout.button.Button(
                        ("Reset"),
                        buttontype="secondary",
                        islink=True,
                        href=self.request.path,
                    ),
                    layout.button.Button(
                        ("Filter"),
                        type="submit",
                    ),
                    style="display: flex; justify-content: flex-end; margin-top: 24px",
                    _class="bx--modal-footer",
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
            style="background-color: #fff",
        )


# ADD SETTING VIEWS AND REGISTER URLS -------------------------------------------


@aslayout
def generalsettings(request):
    layoutobj = layouts.generalsettings(request)
    if models.Person.objects.filter(id=settings.OWNER_PERSON_ID).exists():
        form = generate_form(
            request,
            models.LegalPerson,
            layoutobj,
            models.Person.objects.filter(id=settings.OWNER_PERSON_ID).first(),
        )

        if request.method == "POST":
            if form.is_valid():
                form.save()

        return hg.BaseElement(
            hg.H3(_("Settings")),
            hg.H4(_("General")),
            hg.H5(_("Information about our organization")),
            layout.form.Form(form, layoutobj, style="max-width: 480px"),
        )
    return hg.BaseElement(
        hg.H3(_("Settings")),
        hg.H4(_("General")),
        hg.H5(_("Information about our organization")),
        _(
            "The django setting BASXCONNECT.OWNER_PERSON_ID needs to be set to an existing person in order to be able to edit this screen"
        ),
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
    return layouts.personsettings(request)


@aslayout
def relationshipssettings(request):
    return layouts.relationshipssettings(request)


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


class CustomHighlighter(Highlighter):
    def find_window(self, highlight_locations):
        return (0, self.max_length)


# Search view
# simple person search view, for use with ajax calls
def searchperson(request):
    query = request.GET.get("q")
    highlight = CustomHighlighter(query)

    if not query:
        return HttpResponse("")

    objects = [
        result.object
        for result in SearchQuerySet()
        .models(models.Person)
        .autocomplete(name_auto=query)
        .filter_or(personnumber=query)
        if result.object
    ]

    ret = _("No results")

    if objects:
        ret = hg.UL(
            hg.Iterator(
                objects,
                "object",
                hg.LI(
                    hg.F(
                        lambda c, e: mark_safe(
                            highlight.highlight(c["object"].personnumber)
                        )
                    ),
                    " ",
                    hg.F(
                        lambda c, e: mark_safe(
                            highlight.highlight(c["object"].search_index_snippet())
                        )
                    ),
                    style="cursor: pointer; padding: 0.5rem;",
                    onclick=hg.BaseElement(
                        "document.location = '",
                        hg.F(
                            lambda c, e: reverse_model(
                                c["object"], "edit", kwargs={"pk": c["object"].pk}
                            )
                        ),
                        "'",
                    ),
                    onmouseenter="this.style.backgroundColor = 'lightgray'",
                    onmouseleave="this.style.backgroundColor = 'initial'",
                ),
            )
        )
    return HttpResponse(
        hg.DIV(
            ret,
            _class="raised",
            style="margin-bottom: 1rem; padding: 16px 0 48px 48px; background-color: #fff",
        ).render({})
    )
