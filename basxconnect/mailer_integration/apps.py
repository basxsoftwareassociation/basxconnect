from django.apps import AppConfig
from django.core.checks import Error, register


class MailerIntegrationConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "basxconnect.mailer_integration"


@register()
def check_mailchimp_settings(app_configs, **kwargs):
    required_settings = [
        "MAILCHIMP_API_KEY",
        "MAILCHIMP_SERVER",
        "MAILCHIMP_LIST_ID",
        "MAILCHIMP_SEGMENT_ID",
        "MAILCHIMP_INTERESTS_CATEGORY_ID",
    ]
    errors = []
    for setting in required_settings:
        errors.extend(_check_setting(setting))

    return errors


def _check_setting(required_setting):
    from django.conf import settings

    if not hasattr(settings, required_setting):
        error = Error(
            f"setting.{required_setting} is not defined",
            id=f"basxconnect.mailer_integration.ERROR{required_setting}",
        )
        return [error]
    else:
        return []
