from typing import Any, List

import mailchimp_marketing
from django.conf import settings

from basxconnect.mailer_integration.abstract import abstract_datasource
from basxconnect.mailer_integration.abstract.abstract_person_reader import PersonReader
from basxconnect.mailer_integration.mailchimp import person_reader


class MailchimpDatasource(abstract_datasource.Datasource):
    def __init__(self) -> None:
        self.client = mailchimp_marketing.Client()
        self.client.set_config(
            {"api_key": settings.MAILCHIMP_API_KEY, "server": settings.MAILCHIMP_SERVER}
        )
        self._person_reader = person_reader.MailchimpPersonReader()

    def get_persons(self) -> List[Any]:
        swiss_segment = self.client.lists.get_segment_members_list(
            list_id=settings.MAILCHIMP_LIST_ID,
            segment_id=settings.MAILCHIMP_SEGMENT_ID,
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
        return swiss_segment["members"]

    def person_reader(self) -> PersonReader:
        return self._person_reader

    def tag(self) -> str:
        return "Imported from Mailchimp"
