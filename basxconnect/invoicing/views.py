import htmlgenerator as hg
from basxbread import layout, utils
from basxbread.contrib.document_templates.models import DocumentTemplate
from django import forms, http
from django.contrib import messages
from django.core.mail import EmailMessage
from django.shortcuts import get_object_or_404
from django.utils.timezone import now
from django.utils.translation import gettext_lazy as _
from dynamic_preferences.registries import global_preferences_registry

from .models import Invoice


class EmailEntry(forms.Form):
    recipient = forms.EmailField()


EmailsFormset = forms.formset_factory(EmailEntry, can_delete=True, extra=0)


class SendForm(forms.Form):
    subject = forms.CharField()
    body = forms.CharField(widget=forms.Textarea)
    template = forms.ModelChoiceField(
        queryset=DocumentTemplate.objects.filter(
            model__app_label="basxconnect_invoicing", model__model="invoice"
        )
    )


def send_message(
    request,
    pk: int,
    subject_template,
    body_template,
    attachment_template,
    is_receipt=False,
):
    invoice = get_object_or_404(Invoice, id=pk)
    global_preferences = global_preferences_registry.manager()

    our_company_name = global_preferences["general__organizationname"]
    preferred_email_type = global_preferences["invoicing__default_invoice_email_type"]

    emails = invoice.client.core_email_list.all()
    if preferred_email_type is not None:
        emails = emails.filter(type=preferred_email_type)
    else:
        emails = emails[:1]
    initial_emails = (
        [{"recipient": email.email} for email in emails]
        if emails.exists()
        else [{"recipient": ""}]
    )
    subject = utils.jinja_render(
        subject_template, invoice=invoice, our_company_name=our_company_name
    )
    body = utils.jinja_render(
        body_template, invoice=invoice, our_company_name=our_company_name
    )

    send_form = SendForm(
        initial={
            "subject": subject,
            "body": body,
            "template": attachment_template,
        }
    )
    recipient_formset = EmailsFormset(initial=initial_emails)
    if request.method == "POST":
        send_form = SendForm(
            request.POST,
            initial={
                "subject": subject,
                "body": body,
                "template": attachment_template,
            },
        )
        recipient_formset = EmailsFormset(request.POST, initial=initial_emails)
        if send_form.is_valid() and recipient_formset.is_valid():
            email = EmailMessage(
                subject=send_form.cleaned_data["subject"],
                body=send_form.cleaned_data["body"],
                to=[recp["recipient"] for recp in recipient_formset.cleaned_data],
            )
            filename, data = send_form.cleaned_data["template"].generate_document_pdf(
                invoice
            )
            email.attach(filename, data, "application/pdf")
            email.send()
            if is_receipt:
                invoice.receipt_sent = now().date()
            else:
                invoice.invoice_sent = now().date()
            invoice.save()
            messages.success(request, _("Email successfully sent"))
            return http.HttpResponse("Ok")

    return hg.DIV(
        layout.forms.Form(
            send_form,
            hg.DIV(
                layout.forms.helpers.Label(_("Recepients")),
                layout.forms.Formset.as_plain(
                    recipient_formset,
                    layout.forms.FormField("recipient", no_wrapper=True, no_label=True),
                    add_label=_("Add recipient"),
                ),
                style="max-width: 20rem",
            ),
            hg.DIV(
                layout.forms.FormField("subject", style="width: 100%"),
                layout.forms.FormField("body", style="width: 100%"),
                layout.forms.FormField("template"),
            ),
        )
    )


@utils.aslayout
def send_invoice(request, pk: int):
    global_preferences = global_preferences_registry.manager()
    return send_message(
        request,
        pk,
        global_preferences["invoicing__invoice_message_subject_template"],
        global_preferences["invoicing__invoice_message_body_template"],
        global_preferences["invoicing__default_invoice_template"],
    )


@utils.aslayout
def send_receipt(request, pk: int):
    global_preferences = global_preferences_registry.manager()
    return send_message(
        request,
        pk,
        global_preferences["invoicing__receipt_message_subject_template"],
        global_preferences["invoicing__receipt_message_body_template"],
        global_preferences["invoicing__default_receipt_template"],
        is_receipt=True,
    )
