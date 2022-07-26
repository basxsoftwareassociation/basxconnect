import datetime

from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone

from basxconnect.core.models import Person
from basxconnect.mailer_integration.abstract.mailer import MailerPerson
from basxconnect.mailer_integration.models import Subscription
from basxconnect.mailer_integration.settings import MAILER


@receiver(post_save, sender=Person)
def update_subscription_active(sender, instance: Person, created, **kwargs):

    if hasattr(instance, "core_email_list"):
        for email in instance.core_email_list.all():
            if hasattr(email, "subscription"):
                if (
                    instance.active
                    and not instance.deleted
                    and email.subscription.status == "archived"
                ):
                    email.subscription.status = (
                        email.subscription.status_before_archiving
                    )
                    email.subscription.status_before_archiving = None
                    MAILER.add_person(
                        MailerPerson.from_subscription(email.subscription)
                    )
                    email.subscription.save()
                elif (
                    not instance.active or instance.deleted
                ) and email.subscription.status != "archived":
                    email.subscription.status_before_archiving = (
                        email.subscription.status
                    )
                    email.subscription.status = "archived"
                    MAILER.delete_person(email.email)
                    email.subscription.save()

            from dynamic_preferences.registries import global_preferences_registry

            if (
                global_preferences_registry.manager()[
                    "mailchimp__automatically_subscribe_new_persons"
                ]
                and not hasattr(email, "subscription")
                and instance.preferred_language != ""
                and instance.tags.filter(term="Newsletter").count() == 1
                and instance.history.last().history_date + datetime.timedelta(days=1)
                >= timezone.now()
            ):
                subscription = Subscription.objects.create(
                    email=email,
                    status="subscribed",
                    language=instance.preferred_language,
                )
                MAILER.add_person(MailerPerson.from_subscription(subscription))
