import htmlgenerator as hg
from bread import layout as _layout
from bread import menu
from bread.forms.forms import generate_form
from bread.menu import Link
from bread.utils.urls import aslayout, reverse, reverse_model
from bread.views import BrowseView, EditView, ReadView, layoutasreadonly
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
        Link(
            reverse_model(models.Person, "bulkexport"),
            label="Excel",
            icon="download",
        ),
    )
    searchurl = reverse("basxconnect.core.views.searchperson")
    rowclickaction = "read"

    def get_settingspanel(self):
        return hg.DIV(
            hg.DIV(
                hg.DIV(
                    hg.DIV(_layout.helpers.Label(_("Categories"))),
                    hg.DIV(
                        hg.DIV(
                            _layout.checkbox.Checkbox(
                                _("Natural Persons"),
                                widgetattributes={
                                    "value": "_maintype == &quot;naturalperson&quot;",
                                },
                            ),
                            *[
                                _layout.checkbox.Checkbox(
                                    term.term,
                                    widgetattributes={
                                        "value": f"_type == {term.id}",
                                    },
                                    style="padding-left: 1rem",
                                )
                                for term in models.Term.objects.filter(
                                    category__slug="naturaltype"
                                )
                            ],
                            hg.DIV(style="margin-top: 1rem"),
                            _layout.checkbox.Checkbox(
                                _("Person Associations"),
                                widgetattributes={
                                    "value": "_maintype == &quot;personassociation&quot;",
                                },
                            ),
                            *[
                                _layout.checkbox.Checkbox(
                                    term.term,
                                    widgetattributes={
                                        "value": f"_type == {term.id}",
                                    },
                                    style="padding-left: 1rem",
                                )
                                for term in models.Term.objects.filter(
                                    category__slug="associationtype"
                                )
                            ],
                            style="margin-right: 1rem",
                        ),
                        hg.DIV(
                            _layout.checkbox.Checkbox(
                                _("Legal Persons"),
                                widgetattributes={
                                    "value": "_maintype == &quot;legalperson&quot;",
                                },
                            ),
                            *[
                                _layout.checkbox.Checkbox(
                                    term.term,
                                    widgetattributes={
                                        "value": f"_type == {term.id}",
                                    },
                                    style="padding-left: 1rem",
                                )
                                for term in models.Term.objects.filter(
                                    category__slug="legaltype"
                                )
                            ],
                        ),
                        style="display: flex",
                    ),
                    onclick="this.value = '(' + $$('input[checked]', this).map((i) => i.value).join(') or (') + ')'",
                    data_filter_group=True,
                    style="border-right: #ccc solid 1px;",
                    _class="bx--tile",
                ),
                hg.DIV(
                    hg.DIV(_layout.helpers.Label(_("Tags"))),
                    *[
                        _layout.checkbox.Checkbox(
                            term.term,
                            widgetattributes={
                                "value": f"categories == {term.id}",
                            },
                        )
                        for term in models.Term.objects.filter(
                            category__slug="category"
                        )
                    ],
                    onclick="this.value = '(' + $$('input[checked]', this).map((i) => i.value).join(') or (') + ')'",
                    data_filter_group=True,
                    style="border-right: #ccc solid 1px",
                    _class="bx--tile",
                ),
                hg.DIV(
                    hg.DIV(_layout.helpers.Label(_("Languages"))),
                    *[
                        _layout.checkbox.Checkbox(
                            lang[1],
                            widgetattributes={
                                "value": f"preferred_language == &quot;{lang[0]}&quot;",
                            },
                        )
                        for lang in settings.PREFERRED_LANGUAGES
                    ],
                    onclick="this.value = '(' + $$('input[checked]', this).map((i) => i.value).join(') or (') + ')'",
                    data_filter_group=True,
                    style="border-right: #ccc solid 1px",
                    _class="bx--tile",
                ),
                hg.DIV(
                    hg.DIV(_layout.helpers.Label(_("Status"))),
                    _layout.checkbox.Checkbox(
                        _("Active"),
                        widgetattributes={"value": "active == True"},
                    ),
                    _layout.checkbox.Checkbox(
                        _("Inactive"),
                        widgetattributes={"value": "active == False"},
                    ),
                    onclick="this.value = '(' + $$('input[checked]', this).map((i) => i.value).join(') or (') + ')'",
                    data_filter_group=True,
                    _class="bx--tile",
                ),
                style="display: flex; margin: -1rem; padding-bottom: 2rem",
                onclick="this.value = '(' + $$('div[data-filter-group]', this).filter((i) => Boolean(i.value)).map((i) => i.value).join(') and (') + ')'",
            ),
            hg.DIV(
                _layout.button.Button(("Filter"), style="float: right", aslink=True),
                _layout.button.Button(
                    ("Reset"), buttontype="secondary", style="float: right"
                ),
                _layout.button.Button(
                    ("Cancel"),
                    buttontype="ghost",
                    style="float: right",
                    onclick="this.parentElement.parentElement.parentElement.parentElement.style.display = 'none'",
                ),
                style="margin-bottom: 2rem; margin-right: -1rem",
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
