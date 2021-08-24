import hashlib
from typing import List

import mailchimp_marketing
from django.conf import settings

from basxconnect.core.models import Email
from basxconnect.mailer_integration.abstract import abstract_datasource
from basxconnect.mailer_integration.abstract.abstract_datasource import (
    MailerPerson,
    MailingInterest,
)
from basxconnect.mailer_integration.mailchimp.parsing import (
    create_mailer_person_from_raw,
)
from basxconnect.mailer_integration.models import Interest


class MailchimpDatasource(abstract_datasource.Datasource):
    def __init__(self) -> None:
        self.client = mailchimp_marketing.Client()
        self.client.set_config(
            {"api_key": settings.MAILCHIMP_API_KEY, "server": settings.MAILCHIMP_SERVER}
        )

    def get_persons(self) -> List[MailerPerson]:
        segment = self.client.lists.get_segment_members_list(
            list_id=settings.MAILCHIMP_LIST_ID,
            segment_id=settings.MAILCHIMP_SEGMENT_ID,
            count=getattr(settings, "MAILCHIMP_MAX_SYNC_COUNT", 1000),
            include_cleaned=True,
            include_transactional=True,
            include_unsubscribed=True,
            # TODO: Find out why this does not work. Would be nice to request as little data as possible.
            # fields=[
            #     "email_address",
            #     "merge_fields.FNAME",
            #     "merge_fields.LNAME",
            # ],
        )
        return [
            create_mailer_person_from_raw(raw_person)
            for raw_person in segment["members"]
        ]

    def put_person(self, email: Email):
        email_hash = hashlib.md5(str(email.email).lower().encode()).hexdigest()
        interests = dict(
            [(interest.external_id, False) for interest in Interest.objects.all()]
        )
        for interest in email.mailingpreferences.interests.all():
            interests[interest.external_id] = True

        self.client.lists.set_list_member(
            settings.MAILCHIMP_LIST_ID,
            email_hash,
            {
                "email_address": email.email,
                "status_if_new": email.mailingpreferences.status,
                "status": email.mailingpreferences.status,
                "interests": interests,
            },
        )

    def get_interests(self):
        return [
            MailingInterest(interest["id"], interest["name"])
            for interest in self.client.lists.list_interest_category_interests(
                settings.MAILCHIMP_LIST_ID,
                settings.MAILCHIMP_INTERESTS_CATEGORY_ID,
            )["interests"]
        ]

    def tag(self) -> str:
        return "Imported from Mailchimp"
