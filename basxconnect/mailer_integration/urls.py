from bread.utils.urls import autopath, default_model_paths, model_urlname

import basxconnect.mailer_integration.views
from basxconnect.mailer_integration import models

urlpatterns = [
    autopath(basxconnect.mailer_integration.views.mailer_synchronization_view),
    autopath(
        basxconnect.mailer_integration.views.EditSubscriptionView.as_view(
            model=models.Subscription,
        ),
        urlname=model_urlname(models.Subscription, "ajax_edit"),
    ),
    autopath(
        basxconnect.mailer_integration.views.AddSubscriptionView.as_view(
            model=models.Subscription,
        ),
        urlname=model_urlname(models.Subscription, "ajax_add"),
    ),
    *default_model_paths(models.SynchronizationResult),
]
