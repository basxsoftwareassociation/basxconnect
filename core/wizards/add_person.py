from django import forms
from django.apps import apps
from django.http import HttpResponseRedirect
from formtools.wizard.views import SessionWizardView

from bread import layout
from bread.forms.forms import breadmodelform_factory

from ..models import NaturalPerson, Person, Term


class SearchForm(forms.Form):
    name_of_existing_person = forms.CharField(max_length=255, required=False)


class ChooseType(forms.Form):
    PERSON_TYPES = {
        "core.Person": Person._meta.model_name.title(),
        "core.NaturalPerson": NaturalPerson._meta.model_name.title(),
    }
    persontype = forms.TypedChoiceField(
        choices=tuple(PERSON_TYPES.items()),
        coerce=lambda a: apps.get_model(a),
        empty_value=None,
    )


class ChooseSubType(forms.Form):
    subtype = forms.ModelChoiceField(queryset=Term.objects.all())

    def __init__(self, persontype, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["subtype"].queryset = Term.objects.filter()


class CreateNaturalPerson(forms.Form):
    subject = forms.CharField(max_length=100)


class CreateJuristicPerson(forms.Form):
    subject = forms.CharField(max_length=100)


naturalperson_form = breadmodelform_factory(
    request=None, model=NaturalPerson, layout=layout.DIV("hi")
)
naturalperson_form.layout = layout.DIV("hi")


class AddPersonWizard(SessionWizardView):
    form_list = [SearchForm, ChooseType, ChooseSubType, naturalperson_form]
    template_name = "core/wizards/add_person.html"

    def get_form_kwargs(self, step):
        if step == "2":
            return {"persontype": self.get_cleaned_data_for_step("1")["persontype"]}
        return super().get_form_kwargs()

    def done(self, form_list, **kwargs):
        print(form_list)
        return HttpResponseRedirect(redirect_to="/")
