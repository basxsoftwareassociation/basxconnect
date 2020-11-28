from django import forms
from django.apps import apps
from django.shortcuts import redirect
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from formtools.wizard.views import NamedUrlSessionWizardView

from bread import layout
from bread.forms.forms import breadmodelform_factory
from bread.utils import pretty_modelname

from ..models import JuristicPerson, NaturalPerson, Person, PersonAssociation, Term


def generate_wizard_form(formlayout):
    # needs to be rendered in view of type NamedUrlSessionWizardView in order to work correctly
    def go_back_url(element, context):
        url = reverse(
            context["request"].resolver_match.view_name,
            kwargs={"step": context["wizard"]["steps"].prev},
        )
        return f"document.location='{url}'"

    return layout.form.Form(
        layout.C("wizard.form"),
        layout.form.Form(
            layout.C("wizard.management_form"),
            layout.form.FormField("current_step"),
            standalone=False,
        ),
        formlayout,
        layout.DIV(
            layout.DIV(
                layout.If(
                    layout.C("wizard.steps.prev"),
                    layout.button.Button(
                        _("Back"),
                        buttontype="secondary",
                        onclick=layout.F(go_back_url),
                    ),
                ),
                layout.If(
                    layout.F(
                        lambda e, c: c["wizard"]["steps"].last
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
        label=_("Check for existing entries"),
        max_length=255,
        required=False,
    )

    layout = generate_wizard_form(layout.form.FormField("name_of_existing_person"))


class ChooseType(forms.Form):
    PERSON_TYPES = {
        "core.NaturalPerson": pretty_modelname(NaturalPerson),
        "core.JuristicPerson": pretty_modelname(JuristicPerson),
        "core.PersonAssociation": pretty_modelname(PersonAssociation),
    }
    persontype = forms.TypedChoiceField(
        label=_("Type of person"),
        choices=tuple(PERSON_TYPES.items()),
        coerce=lambda a: apps.get_model(a),
        empty_value=None,
    )

    layout = generate_wizard_form(layout.form.FormField("persontype"))


class ChooseSubType(forms.Form):
    ALLOWED_SUBTYPE_CATEGORY = {
        Person: None,
        NaturalPerson: None,
        JuristicPerson: "legaltype",
        PersonAssociation: "associationtype",
    }
    subtype = forms.ModelChoiceField(
        label=_("Subtype of person"), queryset=Term.objects.all()
    )

    def __init__(self, persontype, *args, **kwargs):
        super().__init__(*args, **kwargs)
        subtype_category = ChooseSubType.ALLOWED_SUBTYPE_CATEGORY.get(persontype)
        if subtype_category is None:
            self.fields = {}
        else:
            self.fields["subtype"].queryset = Term.objects.filter(
                category__slug=subtype_category
            )

    layout = generate_wizard_form(layout.form.FormField("subtype"))


class AddPersonInformation(forms.Form):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    layout = generate_wizard_form(layout.DIV("Please select a person type first"))


class ConfirmNewPerson(forms.Form):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    layout = generate_wizard_form(layout.DIV("Please select a person type first"))


def generate_add_form_for(model):
    ADD_LAYOUTS = {
        NaturalPerson: layout.DIV(
            layout.form.FormField("first_name"), layout.form.FormField("last_name")
        ),
        JuristicPerson: layout.DIV(
            layout.form.FormField("name"), layout.form.FormField("name_addition")
        ),
        PersonAssociation: layout.DIV(layout.form.FormField("name")),
    }

    form = breadmodelform_factory(
        request=None, model=model, layout=ADD_LAYOUTS.get(model, layout.DIV())
    )
    form.layout = generate_wizard_form(ADD_LAYOUTS.get(model, layout.DIV()))
    return form


class AddPersonWizard(NamedUrlSessionWizardView):
    kwargs = {"url_name": "core:person:add_wizard", "urlparams": {"step": "str"}}
    urlparams = None

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
    template_name = "core/wizards/add_person.html"
    condition_dict = {
        "Subtype": lambda wizard: ChooseSubType.ALLOWED_SUBTYPE_CATEGORY.get(
            (wizard.get_cleaned_data_for_step("Type") or {}).get("persontype")
        )
    }

    def get_person_type(self):
        return (self.get_cleaned_data_for_step("Type") or {}).get("persontype")

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        steps = []

        for i, step in enumerate(self.get_form_list().keys()):
            status = "incomplete"
            if i < self.steps.index:
                status = "complete"
            if step == self.steps.current:
                status = "current"
            steps.append((_(step), status))

        context["progress_indicator"] = layout.progress_indicator.ProgressIndicator(
            steps,
            style="margin-bottom: 2rem",
        )
        return context

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
                    form = generate_add_form_for(persontype)(data, files)
                else:
                    form = generate_add_form_for(persontype)(
                        data,
                        files,
                        initial=self.get_cleaned_data_for_step("Information"),
                    )
        return form

    def done(self, form_list, **kwargs):
        # in case the new person had a subtype set, we need to set the attribute here
        subtype = (self.get_cleaned_data_for_step("Subtype") or {}).get("subtype")
        if subtype:
            newperson = list(form_list)[-1].instance.type = subtype
        newperson = list(form_list)[-1].save()
        return redirect(f"core:{newperson._meta.model_name}:edit", pk=newperson.pk)
