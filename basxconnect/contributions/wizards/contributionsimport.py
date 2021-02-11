import os

import htmlgenerator as hg
from bread import layout
from bread.utils.urls import reverse_model
from bread.views import generate_wizard_form
from django import forms
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.shortcuts import redirect
from django.utils.translation import gettext_lazy as _
from formtools.wizard.views import NamedUrlSessionWizardView

from .. import models


class UploadForm(forms.Form):
    title = _("Upload a file")
    importfile = forms.FileField(
        label=_("File to import"), help_text=_("Choose a CSV file"), required=False
    )
    do_not_import_duplicated = forms.BooleanField(
        label=_("Filter out duplicates"), required=False
    )
    _layout = hg.BaseElement(
        layout.form.FormField("importfile"),
        layout.helpers.Label(_("Import options")),
        layout.form.FormField("do_not_import_duplicated"),
    )


class AssignmentForm(forms.Form):
    title = _("Assignment")
    _layout = hg.BaseElement("Assignment")


class FinishedForm(forms.Form):
    title = _("Finished")
    _layout = hg.BaseElement("Finished")


# The WizardView contains mostly control-flow logic and some configuration
class ContributionsImportWizard(NamedUrlSessionWizardView):
    kwargs = {"url_name": "core:person:add_wizard", "urlparams": {"step": "str"}}
    urlparams = (("step", str),)
    file_storage = FileSystemStorage(
        location=os.path.join(settings.MEDIA_ROOT, "wizards")
    )

    form_list = [
        ("upload_file", UploadForm),
        ("assignment", AssignmentForm),
        ("finished", FinishedForm),
    ]
    # translation detection
    template_name = "contributions/wizards/import.html"
    layout = hg.BaseElement()

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context["layout"] = lambda request: generate_wizard_form(
            self,
            _("Import contributions"),
            self.get_form().title,
            self.get_form()._layout,
        )
        return context

    def done(self, form_list, **kwargs):
        return redirect(reverse_model(models.Person, "browse"))
