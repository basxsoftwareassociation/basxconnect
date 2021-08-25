from bread.utils.urls import autopath

import basxconnect.mailer_integration.views
from basxconnect.mailer_integration import models

urlpatterns = [
    autopath(basxconnect.mailer_integration.views.mailchimp_view),
    autopath(
        basxconnect.mailer_integration.views.EditMailingPreferencesView.as_view(
            model=models.MailingPreferences
        )
    ),
    autopath(
        basxconnect.mailer_integration.views.AddMailingPreferencesView.as_view(
            model=models.MailingPreferences
        )
    ),
]
