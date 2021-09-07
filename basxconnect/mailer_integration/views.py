import traceback

import bread.layout.components.notification
import htmlgenerator as hg
from bread import layout, menu
from bread.layout.components.form import Form
from bread.utils import aslayout, reverse_model
from bread.utils.links import Link
from bread.views import AddView, EditView
from django import forms
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _

from basxconnect.core.views import menu_views
from basxconnect.mailer_integration import download_data
from basxconnect.mailer_integration.abstract.abstract_datasource import MailerPerson
from basxconnect.mailer_integration.mailchimp import datasource


@aslayout
def mailchimp_view(request):
    if request.method == "POST":
        try:
            sync_result = download_data.download_persons(
                datasource.MailchimpDatasource()
            )
            notification = bread.layout.components.notification.InlineNotification(
                "Success",
                f"Synchronized mailing preferences for {sync_result.total_synchronized_persons} Mailchimp "
                f"contacts. {sync_result.new_persons} new persons were added to the BasxConnect database. "
                + (
                    "The following mailchimp contacts are not yet in our database but were also not "
                    "added because they were invalid:"
                    ", ".join(sync_result.invalid_new_persons)
                    if len(sync_result.invalid_new_persons) > 0
                    else ""
                ),
            )
        except Exception:
            notification = bread.layout.components.notification.InlineNotification(
                "Error",
                f"An error occured during synchronization. {traceback.format_exc()}",
                kind="error",
            )
    else:
        notification = None

    return Form.wrap_with_form(
        forms.Form(),
        hg.If(notification is not None, notification),
        submit_label="Synchronize with Mailchimp",
    )


menu.registeritem(
    menu.Item(
        Link(
            reverse_lazy("basxconnect.mailer_integration.views.mailchimp_view"),
            _("Mailchimp"),
        ),
        menu_views.settingsgroup,
    )
)


class AddMailingPreferencesView(AddView):
    def get_success_url(self):
        return reverse_model(
            self.object.email.person, "read", kwargs={"pk": self.object.email.person.pk}
        )

    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        datasource.MailchimpDatasource().put_person(
            MailerPerson.from_mailing_preferences(self.object)
        )
        return response


class EditMailingPreferencesView(EditView):
    fields = ["interests"]

    def get_success_url(self):
        return reverse_model(
            self.object.email.person, "read", kwargs={"pk": self.object.email.person.pk}
        )

    def post(self, request, *args, **kwargs):
        result = super().post(request, *args, **kwargs)
        # TODO: https://github.com/basxsoftwareassociation/basxconnect/issues/140
        datasource.MailchimpDatasource().put_person(
            MailerPerson.from_mailing_preferences(self.object)
        )
        return result

    def get_layout(self):
        form_fields = [layout.form.FormField(field) for field in self.fields]
        return hg.DIV(*form_fields)
