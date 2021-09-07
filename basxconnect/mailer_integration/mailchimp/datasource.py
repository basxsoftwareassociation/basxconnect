import hashlib
from typing import List

import mailchimp_marketing
from django.conf import settings

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

    def put_person(self, person: MailerPerson):
        self.client.lists.set_list_member(
            settings.MAILCHIMP_LIST_ID,
            compute_email_hash(person),
            {
                "email_address": person.email,
                "status_if_new": person.status,
                # for the moment we don't alter the mailchimp status in BasxConnect, because it is very
                # critical in Mailchimp and we want to be cautious for now
                # "status": person.status,
                "interests": compute_interests_dict(person),
                "merge_fields": {
                    "FNAME": person.first_name or person.display_name,
                    "LNAME": person.last_name,
                },
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


def compute_interests_dict(person) -> dict:
    interests = dict(
        [(interest.external_id, False) for interest in Interest.objects.all()]
    )
    for interest_id in person.interests_ids:
        interests[interest_id] = True
    return interests


def compute_email_hash(person):
    return hashlib.md5(str(person.email).lower().encode()).hexdigest()
