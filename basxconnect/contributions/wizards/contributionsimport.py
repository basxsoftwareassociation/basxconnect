import os
import traceback

import chardet
import htmlgenerator as hg
import tablib
from bread import layout as _layout
from bread.utils.urls import reverse_model
from bread.views import BreadView, generate_wizard_form
from django import forms
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.core.exceptions import ValidationError
from django.core.files.storage import FileSystemStorage
from django.shortcuts import redirect
from django.utils.html import mark_safe
from django.utils.translation import gettext_lazy as _
from djmoney.contrib.exchange.models import convert_money
from dynamic_preferences.registries import global_preferences_registry
from formtools.wizard.views import NamedUrlSessionWizardView
from moneyed import Money

from basxconnect.core.models import Person

from .. import models

global_preferences = global_preferences_registry.manager()

# specifies whith model field must be taken from which column
# the value None means ignore the field
DEFAULT_COLUMN_MAPPING = {
    "date": 0,
    "note": 1,
    "debitaccount": 2,
    "creditaccount": 3,
    "donornumber": 4,
    "amount": 5,
    "currency": None,
}


def contributions_from_csv(filedata, headers, filter_duplicates):
    global_preferences = global_preferences_registry.manager()
    mapping = settings.BASXCONNECT.get(
        "CONTRIBUTIONS_CSV_COLUMN_MAPPING", DEFAULT_COLUMN_MAPPING
    )
    if not all([key in mapping for key in DEFAULT_COLUMN_MAPPING.keys()]):
        raise ValueError(
            f"Settings CONTRIBUTIONS_CSV_COLUMN_MAPPING needs all keys {DEFAULT_COLUMN_MAPPING.keys()}"
        )

    encoding = chardet.detect(filedata).get("encoding", "utf8") or "utf8"

    ret = []
    for row in tablib.import_set(
        filedata.decode(encoding), headers=headers, format="tsv"
    ):
        data = {k: row[mapping[k]] for k in mapping.keys() if mapping[k] is not None}
        data.setdefault("currency", global_preferences["contributions__currency"])

        externalnumber = data.pop("donornumber")
        person = Person.objects.filter(personnumber=externalnumber)
        if person.exists():
            data["person"] = person.get()
        contribution = models.Contribution(**data)
        contribution.full_clean(exclude=["_import", "person"])
        contribution.donornumber = externalnumber
        if not (
            filter_duplicates
            and models.Contribution.objects.filter(
                date=contribution.date,
                amount=contribution.amount,
                currency=contribution.currency,
                person=contribution.person,
            ).exists()
        ):
            ret.append(contribution)
    return ret


class UploadForm(forms.Form):
    title = _("Upload a file")
    importfile = forms.FileField(
        label=_("File to import"), help_text=_("Choose a CSV file"), required=False
    )
    first_line_is_header = forms.BooleanField(
        label=_("First line is header"), initial=True, required=False
    )
    filter_duplicates = forms.BooleanField(
        label=_("Filter out duplicates"), required=False
    )
    layout = hg.BaseElement(
        _layout.form.FormField("importfile"),
        _layout.helpers.Label(_("Import options")),
        _layout.form.FormField("first_line_is_header"),
        _layout.form.FormField("filter_duplicates"),
    )

    def clean(self):
        ret = super().clean()
        if not ret["importfile"]:
            raise ValidationError(_("Required field"))
        try:
            contributions_from_csv(
                ret["importfile"].read(),
                ret["first_line_is_header"],
                ret["filter_duplicates"],
            )
        except Exception as e:
            traceback.print_exception(type(e), e, e.__traceback__)
            if isinstance(e, forms.ValidationError):
                msg = ["<ul>"]
                for erroritem in e:
                    if isinstance(erroritem, tuple):
                        msg.extend([f"<li>{i}</li>" for i in erroritem[1]])
                    else:
                        msg.append(f"<li>{erroritem}</li>")

                msg = mark_safe("".join(msg + ["</ul>"]))
            else:
                msg = str(e)
            raise forms.ValidationError(mark_safe(_("CSV import problem: ") + msg))
        return ret


class AssignmentForm(forms.Form):
    title = _("Assignment")
    layout = hg.BaseElement(
        _layout.datatable.DataTable(
            columns=(
                _layout.datatable.DataTableColumn(_("Date"), hg.C("row.date"), None),
                _layout.datatable.DataTableColumn(_("Note"), hg.C("row.note"), None),
                _layout.datatable.DataTableColumn(
                    _("Account"), hg.C("row.debitaccount"), None
                ),
                _layout.datatable.DataTableColumn(
                    _("Cost Center"), hg.C("row.creditaccount"), None
                ),
                _layout.datatable.DataTableColumn(
                    _("Person Number"), hg.C("row.person.personnumber"), None
                ),
                _layout.datatable.DataTableColumn(
                    _("Donor Number"), hg.C("row.donornumber"), None
                ),
                _layout.datatable.DataTableColumn(
                    _("Assignment state"),
                    hg.If(
                        hg.C("row.person"),
                        _layout.icon.Icon(
                            "checkmark--filled",
                            size=16,
                            style="fill: currentColor; color: green;",
                        ),
                        _layout.icon.Icon(
                            "warning",
                            size=16,
                            style="fill: currentColor; color: red;",
                        ),
                    ),
                    None,
                ),
                _layout.datatable.DataTableColumn(
                    _("Amount"), hg.C("row.amount_formatted"), None
                ),
            ),
            row_iterator=hg.C("contributions"),
        ).with_toolbar(_("Overview of contributions to import"), hg.C("importfile")),
        hg.DIV(
            hg.DIV(
                hg.DIV(
                    hg.F(lambda c: len(c["contributions"])),
                    " ",
                    _("contributions"),
                    _class="bx--batch-summary",
                ),
                hg.DIV(
                    _("Sum"),
                    hg.SPAN("|", style="margin-left: 1rem; margin-right: 1rem"),
                    hg.F(
                        lambda c: sum(
                            [
                                convert_money(
                                    Money(contr.amount, contr.currency),
                                    global_preferences["contributions__currency"],
                                )
                                for contr in c["contributions"]
                            ]
                        )
                        or Money(0, global_preferences["contributions__currency"])
                    ),
                    style="position: absolute; right: 0; margin-right: 1rem; color: #ffffff",
                ),
                _class="bx--batch-actions--active bx--batch-actions",
            ),
            _class="bx--table-toolbar",
            style="margin-bottom: 4rem",
        ),
        hg.DIV(style="margin-bottom: 2rem"),
        hg.If(
            hg.C("unassigned_contributions"),
            _layout.notification.InlineNotification(
                hg.BaseElement(
                    hg.F(
                        lambda c: len(
                            [c for c in c.get("contributions", ()) if not c.person]
                        )
                    ),
                    _(" contributions could not been assigned"),
                ),
                _(
                    "Please make sure that each entry has contributor number which matches with a person number and do the import again"
                ),
                kind="error",
                lowcontrast=True,
                action=(
                    _("Cancel import"),
                    "window.location = window.location.pathname + '?reset=1'",
                ),
                style="max-width: 100%",
            ),
            _layout.notification.InlineNotification(
                _("Assignment complete"),
                _("Continue in order to complete the import"),
                kind="success",
                style="max-width: 100%",
            ),
        ),
    )


# The WizardView contains mostly control-flow logic and some configuration


class ContributionsImportWizard(
    PermissionRequiredMixin, BreadView, NamedUrlSessionWizardView
):
    urlparams = (("step", str),)
    file_storage = FileSystemStorage(
        location=os.path.join(settings.MEDIA_ROOT, "wizards")
    )
    permission_required = "contributions.add_contributionimport"

    form_list = [
        ("upload_file", UploadForm),
        ("assignment", AssignmentForm),
    ]
    template_name = "bread/base.html"

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)

        upload_file = self.get_cleaned_data_for_step("upload_file")
        context["contributions"] = ()
        if upload_file:
            context["importfile"] = upload_file.get("importfile", None)
            if context["importfile"]:
                context["importfile"].seek(0),
                context["contributions"] = contributions_from_csv(
                    context["importfile"].read(),
                    upload_file.get("first_line_is_header", True),
                    upload_file.get("filter_duplicates", False),
                )

        context["unassigned_contributions"] = len(
            [c for c in context["contributions"] if not c.person]
        )
        # disable "continue" button if there are unassigned contributions
        if (
            self.steps.current == "assignment"
            and context["unassigned_contributions"] > 0
        ):
            for button in self.get_layout().filter(
                lambda element, ancestors: isinstance(element, _layout.button.Button)
                and element.attributes.get("type") == "submit"
            ):
                button.attributes["disabled"] = True
        return context

    def get_layout(self):
        return generate_wizard_form(
            self,
            _("Import contributions"),
            self.get_form().title,
            self.get_form().layout,
        )

    def done(self, form_list, **kwargs):
        context = self.get_context_data(list(form_list)[-1])
        contributionimport = models.ContributionImport.objects.create(
            importfile=context["importfile"], user=self.request.user
        )
        for contribution in context["contributions"]:
            contribution._import = contributionimport
            contribution.save()
        messages.success(
            self.request,
            _("Successfully imported %d contributions") % len(context["contributions"]),
        )
        return redirect(reverse_model(models.ContributionImport, "browse"))

    def get(self, *args, **kwargs):
        if "reset" in self.request.GET:
            self.storage.reset()
            self.storage.current_step = self.steps.first
            return redirect(self.get_step_url(self.steps.current))
        return super().get(*args, **kwargs)
