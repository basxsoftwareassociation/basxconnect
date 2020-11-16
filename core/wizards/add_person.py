from django import forms
from django.http import HttpResponseRedirect
from formtools.wizard.views import SessionWizardView

from ..models import NaturalPerson, Person, Term


class SearchForm(forms.Form):
    subject = forms.CharField(max_length=255, required=False)


PERSON_TYPES = {
    Person._meta.model_name: Person,
    NaturalPerson._meta.model_name: NaturalPerson,
}


class ChooseType(forms.Form):
    persontype = forms.TypedChoiceField(
        choices=tuple(PERSON_TYPES.items()),
        coerce=lambda a: PERSON_TYPES.get(a, None),
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


class AddPersonWizard(SessionWizardView):
    form_list = [
        SearchForm,
        ChooseType,
        ChooseSubType,
        CreateNaturalPerson,
        CreateJuristicPerson,
    ]
    template_name = "core/wizards/add_person.html"

    def get_form_kwargs(self, step):
        if step == "2":
            return {
                "persontype": self.get_form_instance("1").cleaned_data["persontype"]
            }
        return super().get_form_kwargs()

    def done(self, form_list, **kwargs):
        print(form_list)
        return HttpResponseRedirect()
