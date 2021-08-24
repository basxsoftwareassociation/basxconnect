from bread.utils.urls import autopath

import basxconnect.mailer_integration.views

urlpatterns = [
    autopath(basxconnect.mailer_integration.views.mailchimp_view),
]
