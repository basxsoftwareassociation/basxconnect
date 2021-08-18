import bread.layout.components.notification
import htmlgenerator as hg
from bread.layout.components.form import Form
from bread.utils import aslayout
from django import forms

from basxconnect.mailer_integration import download
from basxconnect.mailer_integration.mailchimp import datasource


@aslayout
def mailchimp_view(request):
    if request.method == "POST":
        try:
            sync_result = download.download_persons(datasource.MailchimpDatasource())
            notification = bread.layout.components.notification.InlineNotification(
                "Success",
                f"Synchronized mailing preferences for {sync_result.total_synchronized_persons} Mailchimp "
                f"contacts. {sync_result.new_persons} new persons were added to the BasxConnect database.",
            )
        except Exception as e:
            notification = bread.layout.components.notification.InlineNotification(
                "Error", "An error occured during synchronization.", kind="error"
            )
    else:
        notification = None

    return Form.wrap_with_form(
        forms.Form(),
        hg.If(notification is not None, notification),
        submit_label="Synchronize with Mailchimp",
    )
