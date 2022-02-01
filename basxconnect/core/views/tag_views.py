import bread
import htmlgenerator as hg
from bread import layout as layout
from bread.layout.components.button import Button
from bread.layout.components.modal import Modal, modal_with_trigger
from bread.utils import aslayout, reverse_model
from bread.views import AddView
from django import forms
from django.http import HttpResponseBadRequest, HttpResponseRedirect
from django.utils.translation import gettext_lazy as _
from django.utils.translation import ngettext_lazy
from htmlgenerator import mark_safe

from basxconnect.core import models
from basxconnect.core.models import Term, Vocabulary


class AddTagView(AddView):
    model = models.Term
    fields = ["term", "vocabulary"]

    def form_valid(self, *args, **kwargs):
        ret = super().form_valid(*args, **kwargs)
        ret["HX-Redirect"] = f"{self.request.GET['next']}&new-tag={self.object.id}"
        return ret


@aslayout
def bulk_tag_operation_view(request):
    operation = request.GET["operation"]
    initial = request.GET.get("new-tag")
    if operation not in ["add", "remove"]:
        return HttpResponseBadRequest("invalid GET parameter 'operation'")

    class PersonList(forms.Form):
        persons = forms.ModelMultipleChoiceField(queryset=models.Person.objects.all())

    personlist = PersonList(request.GET)
    if personlist.is_valid():
        persons = [person.pk for person in personlist.cleaned_data["persons"]]
    else:
        return HttpResponseBadRequest("invalid GET parameter 'persons'")

    class BulkTagOperationForm(forms.Form):
        tag = forms.ModelChoiceField(
            queryset=models.Term.objects.filter(vocabulary__slug="tag"),
            required=True,
            initial=initial,
        )

    if request.method == "POST":
        form = BulkTagOperationForm(request.POST)
        if form.is_valid():
            tag = form.cleaned_data.get("tag")
            for person in models.Person.objects.filter(pk__in=persons):
                if operation == "add":
                    person.tags.add(tag)
                else:
                    person.tags.remove(tag)
                person.save()
            return HttpResponseRedirect(reverse_model(models.Person, "browse"))

    form = BulkTagOperationForm()
    count = len(persons)
    if operation == "add":
        header = ngettext_lazy(
            "Add tag to %(count)d person",
            "Add tag to %(count)d persons",
            count,
        ) % {"count": count}
    else:
        header = ngettext_lazy(
            "Remove tag from %(count)d person",
            "Remove tag from %(count)d persons",
            count,
        ) % {"count": count}
    tags_vocabulary_id = (
        getattr(Vocabulary.objects.filter(slug="tag").first(), "id", "") or ""
    )
    return bread.layout.forms.Form(
        form,
        hg.H3(header),
        hg.DIV(
            hg.DIV(bread.layout.forms.FormField("tag")),
            hg.If(
                operation == "add",
                hg.DIV(
                    modal_with_trigger(
                        Modal.with_ajax_content(
                            heading=_("Create new tag"),
                            url=reverse_model(
                                Term,
                                "ajax_add",
                                query={
                                    "vocabulary": tags_vocabulary_id,
                                    "asajax": True,
                                    "next": mark_safe(
                                        reverse_model(
                                            models.Person,
                                            "bulk-tag-operation",
                                            query={
                                                "operation": operation,
                                                "persons": persons,
                                            },
                                        )
                                    ),
                                },
                            ),
                            submitlabel=_("Save"),
                        ),
                        Button,
                        _("Create new tag"),
                        buttontype="ghost",
                        style="margin-bottom: 2rem;",
                        icon="add",
                    ),
                ),
            ),
            style="display:flex;align-items:end;",
        ),
        layout.forms.helpers.Submit(_("Submit")),
    )
