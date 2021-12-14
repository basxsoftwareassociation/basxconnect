import htmlgenerator as hg
from bread import layout
from bread.forms.forms import breadmodelform_factory
from bread.utils import pretty_modelname
from bread.utils.urls import reverse_model
from bread.views import BreadView
from django import forms
from django.apps import apps
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.shortcuts import redirect
from django.urls import reverse, reverse_lazy
from django.utils.translation import gettext_lazy as _
from dynamic_preferences.registries import global_preferences_registry
from formtools.wizard.views import NamedUrlSessionWizardView

from ..models import (
    Email,
    LegalPerson,
    NaturalPerson,
    Person,
    PersonAssociation,
    Postal,
    Term,
)

ADD_FORM_LAYOUTS = {
    NaturalPerson: hg.BaseElement(
        layout.grid.Row(
            layout.grid.Col(layout.form.FormField("first_name")),
            layout.grid.Col(layout.form.FormField("last_name")),
        ),
        layout.grid.Row(
            layout.grid.Col(layout.form.FormField("salutation")),
            layout.grid.Col(layout.form.FormField("gender")),
        ),
    ),
    LegalPerson: hg.DIV(
        layout.form.FormField("name"), layout.form.FormField("name_addition")
    ),
    PersonAssociation: hg.DIV(layout.form.FormField("name")),
}
ADD_ADDRESS_LAYOUT = layout.grid.Grid(
    layout.grid.Row(
        layout.grid.Col(_("Address"), style="font-weight: 700; margin-bottom: 2rem")
    ),
    layout.grid.Row(layout.grid.Col(layout.form.FormField("address"))),
    layout.grid.Row(
        layout.grid.Col(
            layout.form.FormField("postcode"),
        ),
        layout.grid.Col(layout.form.FormField("city")),
    ),
    layout.grid.Row(layout.grid.Col(layout.form.FormField("country"))),
    gutter=False,
)
ADD_EMAIL_LAYOUT = layout.grid.Grid(
    layout.grid.Row(
        layout.grid.Col(_("Email"), style="font-weight: 700; margin-bottom: 2rem")
    ),
    layout.grid.Row(
        layout.grid.Col(
            layout.form.FormField("email", elementattributes={"required": False})
        ),
        layout.grid.Col(layout.form.FormField("type")),
    ),
    gutter=False,
)


def generate_wizard_form(formlayout):
    # needs to be rendered in view of type NamedUrlSessionWizardView in order to work correctly
    def go_back_url(context):
        url = reverse(
            context["request"].resolver_match.view_name,
            kwargs={"step": context["wizard"]["steps"].prev},
        )
        return f"document.location='{url}'"

    return layout.form.Form(
        hg.C("wizard.form"),
        layout.form.Form(
            hg.C("wizard.management_form"),
            layout.form.FormField("current_step"),
            standalone=False,
        ),
        formlayout,
        hg.DIV(
            hg.DIV(
                hg.If(
                    hg.C("wizard.steps.prev"),
                    layout.button.Button(
                        _("Back"),
                        buttontype="secondary",
                        onclick=hg.F(go_back_url),
                    ),
                ),
                hg.If(
                    hg.F(
                        lambda c: c["wizard"]["steps"].last
                        == c["wizard"]["steps"].current
                    ),
                    layout.button.Button(
                        _("Complete"), type="submit", style="margin-left: 1rem"
                    ),
                    layout.button.Button(
                        _("Continue"), type="submit", style="margin-left: 1rem"
                    ),
                ),
            ),
            style="align-items: flex-end",
            _class="bx--form-item",
        ),
    )


class SearchForm(forms.Form):
    name_of_existing_person = forms.CharField(
        label=_("Check for existing people before continuing"),
        max_length=255,
        required=False,
    )

    searchelement = layout.search.Search(
        model=Person,
        widgetattributes={
            "placeholder": _("Start typing to search for a person..."),
            "hx_get": reverse_lazy(
                "basxconnect.core.views.person.search_person_view.searchperson"
            ),
            "hx_trigger": "changed, keyup changed delay:100ms",
            "hx_target": "#search-results",
            "name": "q",
        },
    )
    # clear search field when search box is emptied
    searchelement[0][3].attributes["onclick"] = "$('#search-results').innerHTML = ''"

    title = _("Search person")
    _layout = hg.DIV(
        hg.DIV(
            _(
                "Before a new person can be added it must be confirmed that the person does not exists yet."
            ),
            style="margin-bottom: 2rem",
        ),
        searchelement,
        hg.DIV(id="search-results", style="margin-bottom: 2rem;"),
    )


class ChooseType(forms.Form):
    PERSON_TYPES = {
        "core.NaturalPerson": pretty_modelname(NaturalPerson),
        "core.LegalPerson": pretty_modelname(LegalPerson),
        "core.PersonAssociation": pretty_modelname(PersonAssociation),
    }
    persontype = forms.TypedChoiceField(
        label=_("Type of person"),
        choices=tuple(PERSON_TYPES.items()),
        coerce=lambda a: apps.get_model(a),
        empty_value=None,
    )

    title = _("Choose person main type")
    _layout = hg.BaseElement(
        hg.DIV(
            _("Please choose what type of person you want to add:"),
            style="margin-bottom: 2rem",
        ),
        layout.form.FormField("persontype"),
    )


class ChooseSubType(forms.Form):
    ALLOWED_SUBTYPE_CATEGORY = {
        Person: None,
        NaturalPerson: "naturaltype",
        LegalPerson: "legaltype",
        PersonAssociation: "associationtype",
    }
    subtype = forms.ModelChoiceField(
        label=_("Subtype of person"), queryset=Term.objects.all(), required=False
    )

    def __init__(self, persontype, *args, **kwargs):
        super().__init__(*args, **kwargs)
        subtype_vocabulary = ChooseSubType.ALLOWED_SUBTYPE_CATEGORY.get(persontype)
        if subtype_vocabulary is None:
            self.fields = {}
        else:
            self.fields["subtype"].queryset = Term.objects.filter(
                vocabulary__slug=subtype_vocabulary
            )
            self.fields["subtype"].initial = global_preferences_registry.manager()[
                f"persons__default_{subtype_vocabulary}"
            ]

    title = _("Choose person type")
    _layout = layout.form.FormField("subtype")


class AddPersonInformation(forms.Form):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    title = _("Add person")
    _layout = hg.DIV("Please select a person type first")


class ConfirmNewPerson(forms.Form):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    title = _("Finish")
    _layout = hg.DIV("Please select a person type first")


def generate_add_form_for(model, request, data, files, initial=None):
    form = breadmodelform_factory(
        request=request, model=model, layout=ADD_FORM_LAYOUTS[model]
    )(data, files, initial=initial)

    for fieldname, field in breadmodelform_factory(
        request, Postal, ADD_ADDRESS_LAYOUT
    )().fields.items():
        form.fields[fieldname] = field

    for fieldname, field in breadmodelform_factory(
        request, Email, ADD_EMAIL_LAYOUT
    )().fields.items():
        form.fields[fieldname] = field

    formlayout = hg.BaseElement(
        layout.grid.Grid(
            ADD_FORM_LAYOUTS[model].copy(), style="margin-bottom: 2rem", gutter=False
        ),
        layout.grid.Grid(
            layout.grid.Row(
                layout.grid.Col(ADD_ADDRESS_LAYOUT.copy()),
                layout.grid.Col(ADD_EMAIL_LAYOUT.copy()),
            ),
            gutter=False,
        ),
    )
    form._layout = formlayout
    return form


# The WizardView contains mostly control-flow logic and some configuration
class AddPersonWizard(PermissionRequiredMixin, BreadView, NamedUrlSessionWizardView):
    kwargs = {"url_name": "core:person:add_wizard", "urlparams": {"step": "str"}}
    urlparams = (("step", str),)
    permission_required = "core.add_person"

    form_list = [
        ("Search", SearchForm),
        ("Type", ChooseType),
        ("Subtype", ChooseSubType),
        ("Information", AddPersonInformation),
        ("Confirmation", ConfirmNewPerson),
    ]
    # translation detection
    _("Search")
    _("Type")
    _("Subtype")
    _("Information")
    _("Confirmation")
    condition_dict = {
        "Subtype": lambda wizard: ChooseSubType.ALLOWED_SUBTYPE_CATEGORY.get(
            (wizard.get_cleaned_data_for_step("Type") or {}).get("persontype")
        )
    }

    def get_person_type(self):
        return (self.get_cleaned_data_for_step("Type") or {}).get("persontype")

    def get_steps(self):
        steps = []

        for i, step in enumerate(self.get_form_list().keys()):
            status = "incomplete"
            if i < self.steps.index:
                status = "complete"
            if step == self.steps.current:
                status = "current"
            steps.append((_(step), status))
        return steps

    def get_layout(self):
        return hg.BaseElement(
            hg.H3(_("Add new person")),
            hg.H4(self.get_form().title),
            layout.progress_indicator.ProgressIndicator(
                self.get_steps(),
                style="margin-bottom: 2rem",
            ),
            generate_wizard_form(self.get_form()._layout),
            hg.SCRIPT(
                hg.mark_safe(
                    r"""
                    addressTextarea = document.getElementById("id_address");
                    submitBtn = document.querySelector(".bx--content [type=\"submit\"]");
                    var addressFocused = false;
                    if (addressTextarea !== null) {
                        addressTextarea.addEventListener("focus", e => {
                            addressFocused = true;
                        });
                        addressTextarea.addEventListener("blur", e => {
                            addressFocused = false;
                        });
                    }
                    document.addEventListener("keydown", e => {
                        if (e.code === "Enter" && !addressFocused)
                            submitBtn.click();
                    });
                    """
                )
            ),
        )

    def get_form_kwargs(self, step):
        ret = super().get_form_kwargs()
        if step == "Subtype":
            ret.update({"persontype": self.get_person_type()})
        return ret

    def get_form(self, step=None, data=None, files=None):
        form = super().get_form(step, data, files)
        if step is None:
            step = self.steps.current

        # step 3 and 4 depend on the select type, so we generate the forms dynamically
        if step in ("Information", "Confirmation"):
            persontype = self.get_person_type()
            if persontype:
                if step == "Information":
                    form = generate_add_form_for(
                        persontype,
                        self.request,
                        data,
                        files,
                    )
                else:
                    form = generate_add_form_for(
                        persontype,
                        self.request,
                        data,
                        files,
                        self.get_cleaned_data_for_step("Information"),
                    )
                    form._layout.insert(
                        0,
                        layout.notification.InlineNotification(
                            "",
                            _("Review and confirm the entered information"),
                            lowcontrast=True,
                            hideclosebutton=True,
                        ),
                    )
                    for fieldname in form.fields:
                        form.fields[fieldname].disabled = True
                        form.fields[fieldname].widget.attrs["style"] = "color: #000"
                form.title = _("Add %s") % pretty_modelname(persontype)
        return form

    def done(self, form_list, **kwargs):
        personform = list(form_list)[-1]
        # in case the new person had a subtype set, we need to set the attribute here
        subtype = (self.get_cleaned_data_for_step("Subtype") or {}).get("subtype")
        if subtype:
            personform.instance.type = subtype
        newperson = personform.save()
        newperson.core_postal_list.create(
            **{
                k: v
                for k, v in personform.cleaned_data.items()
                if k in ("address", "city", "postcode", "country")
            }
        )
        if "email" in personform.cleaned_data:
            newperson.core_email_list.create(
                email=personform.cleaned_data["email"],
                type=personform.cleaned_data["type"],
            )

        newperson.save()
        return redirect(
            reverse_model(
                newperson._meta.model,
                "read",
                kwargs={"pk": newperson.pk},
            )
        )
