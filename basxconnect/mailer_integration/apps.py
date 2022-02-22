from django.apps import AppConfig
from django.core.checks import Error, register


class MailerIntegrationConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "basxconnect.mailer_integration"

    def ready(self):
        import basxconnect.mailer_integration.signal_handlers  # noqa
