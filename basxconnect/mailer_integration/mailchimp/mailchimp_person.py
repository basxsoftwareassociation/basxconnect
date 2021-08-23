import logging
from typing import Any, List

import pycountry

from basxconnect.mailer_integration.abstract.abstract_mailer_person import MailerPerson

logger = logging.getLogger(__name__)


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

    def interests_ids(self) -> List[str]:
        interest_indicators = self.raw_person["interests"]
        interests_ids = [
            interest_id
            for interest_id, interested in interest_indicators.items()
            if interested
        ]
        return interests_ids

    def status(self) -> str:
        return self.raw_person["status"]

    def country(self):
        _country = pycountry.countries.get(
            name=self.raw_person["merge_fields"]["MMERGE11"], default=None
        )
        if _country:
            return _country.alpha_2
        else:
            return "CH"

    def postcode(self):
        return self.raw_person["merge_fields"]["MMERGE10"]

    def address(self):
        return self.raw_person["merge_fields"]["MMERGE7"]

    def city(self):
        return self.raw_person["merge_fields"]["MMERGE8"]
