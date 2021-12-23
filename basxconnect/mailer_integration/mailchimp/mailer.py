import hashlib
from typing import List

import mailchimp_marketing
from django.conf import settings
from mailchimp_marketing.api_client import ApiClientError

from basxconnect.mailer_integration.abstract import mailer
from basxconnect.mailer_integration.abstract.mailer import MailerPerson, MailingInterest
from basxconnect.mailer_integration.mailchimp.parsing import (
    create_mailer_person_from_raw,
)
from basxconnect.mailer_integration.models import Interest


class Mailchimp(mailer.AbstractMailer):
    def __init__(self) -> None:
        self.client = mailchimp_marketing.Client()
        self.client.set_config(
            {"api_key": settings.MAILCHIMP_API_KEY, "server": settings.MAILCHIMP_SERVER}
        )

    def name(self) -> str:
        return "Mailchimp"

    def get_person_count(self) -> int:
        return self.client.lists.get_segment(
            list_id=settings.MAILCHIMP_LIST_ID,
            segment_id=settings.MAILCHIMP_SEGMENT_ID,
        )["member_count"]

    def get_persons(self, count: int, offset: int) -> List[MailerPerson]:
        segment = self.client.lists.get_segment_members_list(
            list_id=settings.MAILCHIMP_LIST_ID,
            segment_id=settings.MAILCHIMP_SEGMENT_ID,
            count=count,
            offset=offset,
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

    def delete_person(self, email: str):
        self.client.lists.delete_list_member(
            settings.MAILCHIMP_LIST_ID, compute_email_hash(email)
        )

    def put_person(self, person: MailerPerson, **kwargs):
        email_hash = compute_email_hash(person.email)
        self.client.lists.set_list_member(
            settings.MAILCHIMP_LIST_ID,
            email_hash,
            {
                "email_address": person.email,
                "status_if_new": person.status,
                "interests": compute_interests_dict(person),
                "merge_fields": {
                    "FNAME": person.first_name or person.display_name,
                    "LNAME": person.last_name,
                    **(
                        settings.MAILCHIMP_ADDITIONAL_MERGE_FIELDS(person)
                        if hasattr(settings, "MAILCHIMP_ADDITIONAL_MERGE_FIELDS")
                        else {}
                    ),
                },
                "language": person.language,
                **kwargs,
            },
        )
        if hasattr(settings, "MAILCHIMP_TAG"):
            self.client.lists.update_list_member_tags(
                settings.MAILCHIMP_LIST_ID,
                email_hash,
                {"tags": [{"name": settings.MAILCHIMP_TAG, "status": "active"}]},
            )

    def add_person(self, person: MailerPerson):
        self.put_person(person, status=person.status)

    def email_exists(self, email: str) -> bool:
        try:
            self.client.lists.get_list_member(
                settings.MAILCHIMP_LIST_ID, compute_email_hash(email)
            )
        except ApiClientError as e:
            if e.status_code == 404:
                return False
            raise e
        return True

    def change_email_address(self, old_email: str, new_email: str):
        self.client.lists.update_list_member(
            settings.MAILCHIMP_LIST_ID,
            compute_email_hash(old_email),
            {"email_address": new_email},
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


def compute_email_hash(email):
    # required by mailchimp, ignore security check
    return hashlib.md5(str(email).lower().encode()).hexdigest()  # nosec
