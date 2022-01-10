import bread
import htmlgenerator as hg
from bread import layout as layout
from bread.layout.components.button import Button
from bread.layout.components.modal import modal_with_trigger, Modal
from bread.utils import aslayout, reverse_model, ModelHref
from django import forms
from django.http import HttpResponseBadRequest, HttpResponseRedirect
from django.utils.translation import ngettext_lazy, gettext_lazy as _

from basxconnect.core import models
from basxconnect.core.models import Vocabulary, Term


@aslayout
def bulk_tag_operation_view(request):
    operation = request.GET["operation"]
    if operation not in ["add", "remove"]:
        return HttpResponseBadRequest("invalid GET parameter 'operation'")
    persons = request.GET.getlist("persons")

    class BulkTagOperationForm(forms.Form):
        tag = forms.ModelChoiceField(
            queryset=models.Term.objects.filter(vocabulary__slug="tag"), required=True
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
        header = (
            ngettext_lazy(
                "Add tag to %(count)d person",
                "Add tag to %(count)d persons",
                count,
            )
            % {"count": count}
        )
    else:
        header = (
            ngettext_lazy(
                "Remove tag from %(count)d person",
                "Remove tag from %(count)d persons",
                count,
            )
            % {"count": count}
        )
    tags_vocabulary_id = Vocabulary.objects.filter(slug="tag").first().id or ""
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
                            url=ModelHref(
                                Term,
                                "add",
                                query={
                                    "vocabulary": tags_vocabulary_id,
                                    "asajax": True,
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
