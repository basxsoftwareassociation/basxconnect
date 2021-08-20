import logging
from typing import Any, List

from basxconnect.mailer_integration.abstract.abstract_mailer_person import MailerPerson

logger = logging.getLogger(__name__)

INTERESTS = {"a244484af6": "Newsletter", "d8723b3a79": "Prayer Bulletin"}


class MailchimpPerson(MailerPerson):
    def __init__(self, raw_person: Any) -> None:
        """raw_person can look like this:
        {
            'id': 'bdcba63278c17c44b5b01e0529904aaa',
            'email_address': 'test@gmx.ch',
            'unique_email_id': '06862cfbaa',
            'email_type': 'html',
            'status': 'subscribed',
            'merge_fields': {
                'FNAME': 'Peter', 'PREFNAME': 'Peter', 'LNAME': 'Müller', 'MMERGE7': 'Hauptstr. 26A',
                'MMERGE8': 'Schnotwil', 'MMERGE9': 'SO', 'MMERGE10': '6000', 'MMERGE11': 'Switzerland',
                'MMERGE12': '', 'MMERGE13': '', 'MMERGE14': '', 'MMERGE15': '', 'MMERGE16': '', 'MMERGE17': '',
                'MMERGE3': 'Deutsch', 'MMERGE4': '', 'MMERGE6': '', 'MMERGE18': ''
            }, etc ...
        }
        """
        self.raw_person = raw_person
        super().__init__()

    def first_name(self) -> str:
        return self.raw_person["merge_fields"]["FNAME"]

    def last_name(self) -> str:
        return self.raw_person["merge_fields"]["LNAME"]

    def display_name(self) -> str:
        return f"{self.raw_person['merge_fields']['FNAME']} {self.raw_person['merge_fields']['LNAME']}"

    def email(self) -> str:
        return self.raw_person["email_address"]

    def interests(self) -> List[str]:
        interest_indicators = self.raw_person["interests"]
        interests_ids = [
            interest_id
            for interest_id, interested in interest_indicators.items()
            if interested
        ]
        interests = []
        for _id in interests_ids:
            if _id in INTERESTS:
                interests.append(INTERESTS[_id])
            else:
                logger.error(f"Unknown interest id {_id}")
        return interests

    def status(self) -> str:
        return self.raw_person["status"]
