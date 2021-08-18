from bread.utils.urls import generate_path

import basxconnect.mailer_integration.views

urlpatterns = [
    generate_path(basxconnect.mailer_integration.views.mailchimp_view),
]
