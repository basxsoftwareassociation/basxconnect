import logging
from typing import List

from django.conf import settings

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


# TODO: https://github.com/basxsoftwareassociation/basxconnect/issues/141
def city(raw_person):
    if not raw_person["merge_fields"]["ADDRESS"]:
        return None
    return raw_person["merge_fields"]["ADDRESS"]["city"]


# TODO: https://github.com/basxsoftwareassociation/basxconnect/issues/141
def address(raw_person):
    if not raw_person["merge_fields"]["ADDRESS"]:
        return None
    addr1 = raw_person["merge_fields"]["ADDRESS"]["addr1"]
    addr2 = raw_person["merge_fields"]["ADDRESS"]["addr2"]
    return addr1 + ("\naddr2" if addr2 else "")


# TODO: https://github.com/basxsoftwareassociation/basxconnect/issues/141
def postcode(raw_person):
    if not raw_person["merge_fields"]["ADDRESS"]:
        return None
    return raw_person["merge_fields"]["ADDRESS"]["zip"]


# TODO: https://github.com/basxsoftwareassociation/basxconnect/issues/141
def country(raw_person):
    if not raw_person["merge_fields"]["ADDRESS"]:
        return getattr(settings, "MAILCHIMP_DEFAULT_COUNTRY", "CH")
    return raw_person["merge_fields"]["ADDRESS"]["country"]


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
