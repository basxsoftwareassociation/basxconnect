from typing import List

import mailchimp_marketing
from django.conf import settings

from basxconnect.mailer_integration.abstract import abstract_datasource
from basxconnect.mailer_integration.abstract.abstract_datasource import MailingInterest
from basxconnect.mailer_integration.abstract.abstract_mailer_person import MailerPerson
from basxconnect.mailer_integration.mailchimp.mailchimp_person import MailchimpPerson

URBANMOSAIC_ALL_MEMBERS_LIST_ID = "4606fb0179"
SWISS_SEGMENT_ID = "36705"


class MailchimpDatasource(abstract_datasource.Datasource):
    def __init__(self) -> None:
        self.client = mailchimp_marketing.Client()
        self.client.set_config({"api_key": settings.MAILCHIMP_API_KEY, "server": "us5"})

    def get_persons(self) -> List[MailerPerson]:
        segment = self.client.lists.get_segment_members_list(
            list_id=URBANMOSAIC_ALL_MEMBERS_LIST_ID,
            segment_id=SWISS_SEGMENT_ID,
            count=1000,
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
        return [MailchimpPerson(raw_person) for raw_person in segment["members"]]

    def get_interests(self):
        return [
            MailingInterest(interest["id"], interest["name"])
            for interest in self.client.lists.list_interest_category_interests(
                URBANMOSAIC_ALL_MEMBERS_LIST_ID,
                settings.MAILCHIMP_INTERESTS_CATEGORY_ID,
            )["interests"]
        ]

    def tag(self) -> str:
        return "Imported from Mailchimp"
