from django.db.models.signals import post_save
from django.dispatch import receiver

from basxconnect.core.models import Person
from basxconnect.mailer_integration.abstract.mailer import MailerPerson
from basxconnect.mailer_integration.settings import MAILER


@receiver(post_save, sender=Person)
def update_subscription_active(sender, instance, created, **kwargs):

    if hasattr(instance, "core_email_list"):
        for email in instance.core_email_list.all():
            if hasattr(email, "subscription"):
                if (
                    instance.active
                    and not instance.deleted
                    and not email.subscription.active
                ):
                    email.subscription.active = True
                    MAILER.add_person(
                        MailerPerson.from_subscription(email.subscription)
                    )
                elif email.subscription.active:
                    email.subscription.active = False
                    MAILER.delete_person(email.email)
                email.subscription.save()
