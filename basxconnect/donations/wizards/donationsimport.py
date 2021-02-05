from bread import layout
from bread.utils.urls import reverse_model
from django import forms
from django.shortcuts import redirect
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from formtools.wizard.views import NamedUrlSessionWizardView


def generate_wizard_form(formlayout):
    # needs to be rendered in view of type NamedUrlSessionWizardView in order to work correctly
    def go_back_url(context, element):
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
                        lambda c, e: c["wizard"]["steps"].last
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


class UploadForm(forms.Form):
    title = _("Upload a file")
    _layout = layout.BaseElement("Select file")


class PreviewForm(forms.Form):
    pass


# The WizardView contains mostly control-flow logic and some configuration
class DonationsImportWizard(NamedUrlSessionWizardView):
    kwargs = {"url_name": "core:person:add_wizard", "urlparams": {"step": "str"}}
    urlparams = (("step", str),)

    form_list = [
        ("Upload File", UploadForm),
        ("Preview", PreviewForm),
    ]
    # translation detection
    _("Upload File")
    _("Preview")
    template_name = "donations/wizards/import.html"
    layout = layout.BaseElement()

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context["layout"] = lambda request: generate_wizard_form(
            self.get_form()._layout
        )
        return context

    def done(self, form_list, **kwargs):
        newperson = list(form_list)[-1].save()
        newperson.core_postal_list.create(
            **{
                k: v
                for k, v in list(form_list)[-1].cleaned_data.items()
                if k in ("address", "city", "postcode", "country")
            }
        )
        return redirect(
            reverse_model(
                newperson._meta.model,
                "edit",
                query={"next": "/"},
                kwargs={"pk": newperson.pk},
            )
        )
