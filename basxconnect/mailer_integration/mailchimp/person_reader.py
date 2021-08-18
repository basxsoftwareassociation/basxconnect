# import the logging library
import logging
from typing import Any, List

from basxconnect.mailer_integration.abstract import abstract_person_reader

logger = logging.getLogger(__name__)

INTERESTS = {"a244484af6": "Newsletter", "d8723b3a79": "Prayer Bulletin"}


class MailchimpPersonReader(abstract_person_reader.PersonReader):
    """Reads fields of a raw person coming in from Mailchimp
    e.g.:
    {
        'id': 'bdcba63278c17c44b5b01e0529904aaa',
        'email_address': 'test@gmx.ch',
        'unique_email_id': '06862cfbaa',
        'email_type': 'html',
        'status': 'subscribed',
        'merge_fields': {
            'FNAME': 'Peter',
            'PREFNAME': 'Peter',
            'LNAME': 'Müller',
            'MMERGE7': 'Hauptstr. 26A',
            'MMERGE8': 'Schnotwil',
            'MMERGE9': 'SO',
            'MMERGE10': '6000',
            'MMERGE11': 'Switzerland',
            'MMERGE12': '',
            'MMERGE13': '',
            'MMERGE14': '',
            'MMERGE15': '',
            'MMERGE16': '',
            'MMERGE17': '',
            'MMERGE3': 'Deutsch',
            'MMERGE4': '',
            'MMERGE6': '',
            'MMERGE18': ''
        },
         etc ...
        ]
    }
    """

    @staticmethod
    def interests_of(person: Any) -> List[str]:
        interest_indicators = person["interests"]
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

    @staticmethod
    def status_of(person: Any) -> str:
        return person["status"]

    @staticmethod
    def first_name_of(person: Any) -> str:
        return person["merge_fields"]["FNAME"]

    @staticmethod
    def last_name_of(person: Any) -> str:
        return person["merge_fields"]["LNAME"]

    @staticmethod
    def display_name_of(person: Any) -> str:
        return f"{person['merge_fields']['FNAME']} {person['merge_fields']['LNAME']}"

    @staticmethod
    def email_of(person: Any) -> str:
        return person["email_address"]
