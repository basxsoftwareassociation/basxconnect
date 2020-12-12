import htmlgenerator as hg
from bread import layout, menu
from bread.forms.forms import generate_form
from bread.utils.urls import (
    htmlgeneratorview,
    model_urlname,
    registerurl,
    reverse,
    reverse_model,
)
from bread.views import EditView, register_default_modelviews
from django.http import HttpResponse
from django.utils.html import mark_safe
from django.utils.translation import gettext_lazy as _
from django.views.generic import RedirectView
from haystack.query import SearchQuerySet

from .layouts import person_edit_layout
from .models import (
    Category,
    JuristicPerson,
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
registerurl(model_urlname(Person, "addwizard"))(
    AddPersonWizard.as_view(url_name=model_urlname(Person, "addwizard"))
)
register_default_modelviews(Person, addview=None)
register_default_modelviews(
    NaturalPerson, addview=None, editview=EditView._with(layout=person_edit_layout)
)
register_default_modelviews(JuristicPerson, addview=None)  # uses AddPersonWizard
register_default_modelviews(PersonAssociation, addview=None)  # uses AddPersonWizard
register_default_modelviews(RelationshipType)
register_default_modelviews(Relationship)
register_default_modelviews(Term)
register_default_modelviews(Category)


# ADD SETTING VIEWS AND REGISTER URLS -------------------------------------------


@registerurl
@htmlgeneratorview
def generalsettings(request):
    instance = JuristicPerson.objects.get(id=1)  # must exists due to migration
    form = generate_form(request, JuristicPerson, generalsettings_layout, instance)

    if request.method == "POST":
        if form.is_valid():
            form.save()

    return hg.BaseElement(
        hg.H1(_("General")),
        hg.H2(_("Information about our organization")),
        layout.form.Form(form, generalsettings_layout),
    )


@registerurl
@htmlgeneratorview
def appearancesettings(request):
    return appearancesettings_layout


@registerurl
@htmlgeneratorview
def personssettings(request):
    return personssettings_layout


@registerurl
@htmlgeneratorview
def relationshipssettings(request):
    return relationshipssettings_layout


@registerurl
@htmlgeneratorview
def apikeyssettings(request):
    return apikeyssettings_layout


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
        .models(NaturalPerson, JuristicPerson, PersonAssociation)
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


# LAYOUTS FOR SETTING VIEWS -----------------------------------------------------


def single_item_fieldset(related_field, fieldname, queryset=None):
    """Helper function to show only a single item of a (foreign-key) related item list"""
    return layout.form.FormSetField(
        related_field,
        layout.form.FormField(fieldname),
        formsetinitial={"queryset": queryset},
        can_delete=False,
        max_num=1,
        extra=1,
    )


generalsettings_layout = layout.BaseElement(
    layout.grid.Grid(
        layout.grid.Row(layout.grid.Col(layout.form.FormField("type"))),
        layout.grid.Row(layout.grid.Col(layout.form.FormField("name"))),
        layout.grid.Row(layout.grid.Col(layout.form.FormField("name_addition"))),
    ),
    layout.form.FormSetField(
        "core_postal_list",
        layout.grid.Grid(
            layout.grid.Row(layout.grid.Col(layout.form.FormField("address"))),
            layout.grid.Row(
                layout.grid.Col(layout.form.FormField("supplemental_address"))
            ),
            layout.grid.Row(
                layout.grid.Col(
                    layout.form.FormField("postcode"), breakpoint="lg", width=2
                ),
                layout.grid.Col(
                    layout.form.FormField("city"), breakpoint="lg", width=3
                ),
                layout.grid.Col(
                    layout.form.FormField("country"), breakpoint="lg", width=3
                ),
            ),
        ),
        can_delete=False,
        max_num=1,
        extra=1,
    ),
    layout.grid.Grid(
        layout.grid.Row(
            layout.grid.Col(single_item_fieldset("core_phone_list", "number")),
            layout.grid.Col(single_item_fieldset("core_fax_list", "number")),
        ),
        layout.grid.Row(
            layout.grid.Col(
                single_item_fieldset(
                    "core_email_list",
                    "email",
                )
            ),
            layout.grid.Col(single_item_fieldset("core_web_list", "url")),
        ),
    ),
    layout.form.SubmitButton(_("Save")),
)


appearancesettings_layout = hg.BaseElement(hg.H2(_("Appearance")))

dist = hg.DIV(style="margin-bottom: 2rem")
personssettings_layout = hg.BaseElement(
    hg.H2(_("Persons")),
    # address type
    layout.datatable.DataTable.from_queryset(
        Term.objects.filter(category__slug="addresstype"),
        fields=["term"],
        title=_("Address types"),
        addurl=reverse_model(
            Term,
            "add",
            query={
                "category": Category.objects.get(slug="addresstype").id,
                "next": reverse("basxconnect.core.views.personssettings"),
            },
        ),
        backurl=reverse("basxconnect.core.views.personssettings"),
    ),
    dist,
    # address origin
    layout.datatable.DataTable.from_queryset(
        Term.objects.filter(category__slug="addressorigin"),
        fields=["term"],
        title=_("Address origins"),
        addurl=reverse_model(
            Term,
            "add",
            query={
                "category": Category.objects.get(slug="addressorigin").id,
                "next": reverse("basxconnect.core.views.personssettings"),
            },
        ),
        backurl=reverse("basxconnect.core.views.personssettings"),
    ),
    dist,
    # salutation
    layout.datatable.DataTable.from_queryset(
        Term.objects.filter(category__slug="salutation"),
        fields=["term"],
        title=_("Salutation"),
        addurl=reverse_model(
            Term,
            "add",
            query={
                "category": Category.objects.get(slug="salutation").id,
                "next": reverse("basxconnect.core.views.personssettings"),
            },
        ),
        backurl=reverse("basxconnect.core.views.personssettings"),
    ),
    dist,
)


relationshipssettings_layout = hg.BaseElement(
    hg.H2(_("Relationships")),
    layout.datatable.DataTable.from_queryset(
        RelationshipType.objects.all(),
        fields=["name"],
        addurl=reverse_model(
            RelationshipType,
            "add",
            query={"next": reverse("basxconnect.core.views.relationshipssettings")},
        ),
        backurl=reverse("basxconnect.core.views.relationshipssettings"),
    ),
)


apikeyssettings_layout = hg.BaseElement(hg.H2(_("APK Keys")))
