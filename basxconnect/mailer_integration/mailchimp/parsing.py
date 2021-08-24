import logging
from typing import List

import pycountry

from basxconnect.mailer_integration.abstract.abstract_datasource import MailerPerson

logger = logging.getLogger(__name__)


def create_mailer_person_from_raw(person: str) -> MailerPerson:
    return MailerPerson(
        first_name=first_name(person),
        last_name=last_name(person),
        display_name=display_name(person),
        email=email(person),
        interests_ids=interests_ids(person),
        status=status(person),
        country=country(person),
        postcode=postcode(person),
        address=address(person),
        city=city(person),
    )


def city(raw_person):
    return raw_person["merge_fields"].get("MMERGE8")


def address(raw_person):
    return raw_person["merge_fields"].get("MMERGE7")


def postcode(raw_person):
    return raw_person["merge_fields"].get("MMERGE10")


def country(raw_person):
    _country = pycountry.countries.get(
        name=raw_person["merge_fields"].get("MMERGE11", "CH"), default=None
    )
    if _country:
        return _country.alpha_2
    else:
        return "CH"


def status(raw_person) -> str:
    return raw_person["status"]


def interests_ids(raw_person) -> List[str]:
    interest_indicators = raw_person["interests"]
    interests_ids = [
        interest_id
        for interest_id, interested in interest_indicators.items()
        if interested
    ]
    return interests_ids


def email(raw_person) -> str:
    return raw_person["email_address"]


def display_name(raw_person) -> str:
    return (
        f"{raw_person['merge_fields']['FNAME']} {raw_person['merge_fields']['LNAME']}"
    )


def last_name(raw_person) -> str:
    return raw_person["merge_fields"]["LNAME"]


def first_name(raw_person) -> str:
    return raw_person["merge_fields"]["FNAME"]
