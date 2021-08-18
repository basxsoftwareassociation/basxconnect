from bread.utils.links import Link
from django.apps import AppConfig
from django.urls import reverse_lazy


class MailerIntegrationConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "basxconnect.mailer_integration"

    def ready(self):
        from bread import menu
        from django.utils.translation import gettext_lazy as _

        from basxconnect.core.views import menu_views

        menu.registeritem(
            menu.Item(
                Link(
                    reverse_lazy("basxconnect.mailer_integration.views.mailchimp_view"),
                    _("Mailchimp"),
                ),
                menu_views.settingsgroup,
            )
        )
