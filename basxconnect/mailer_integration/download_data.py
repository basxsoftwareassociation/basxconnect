from typing import NamedTuple

from basxconnect.core import models
from basxconnect.mailer_integration.abstract.abstract_datasource import (
    Datasource,
    MailerPerson,
)
from basxconnect.mailer_integration.models import Interest, MailingPreferences


class SynchronizationResult(NamedTuple):
    new_persons: int
    total_synchronized_persons: int


def download_persons(datasource: Datasource) -> SynchronizationResult:
    interests = datasource.get_interests()
    for interest in interests:
        Interest.objects.get_or_create(external_id=interest.id, name=interest.name)

    mailer_persons = datasource.get_persons()
    datasource_tag = _get_or_create_tag(datasource.tag())
    new_persons = 0
    for mailer_person in mailer_persons:
        matching_email_addresses = list(
            models.Email.objects.filter(
                email=mailer_person.email,
            ).all()
        )
        if len(matching_email_addresses) == 0:
            _save_person(datasource_tag, mailer_person)
            new_persons += 1
        else:
            # if the downloaded email address already exists in our system, update the mailing preference for this email
            # address, without creating a new person in the database
            for email in matching_email_addresses:
                _save_mailing_preferences(email, mailer_person)

    return SynchronizationResult(new_persons, len(mailer_persons))


def _get_or_create_tag(tag: str) -> models.Term:
    tags_category = models.Category.objects.get(slug="category")
    tag, _ = models.Term.objects.get_or_create(term=tag, category_id=tags_category)
    return tag


def _save_person(datasource_tag: models.Term, mailer_person: MailerPerson):
    person = models.NaturalPerson.objects.create(
        first_name=mailer_person.first_name,
        name=mailer_person.display_name,
        last_name=mailer_person.last_name,
    )
    person.categories.add(datasource_tag)
    person.save()
    email = models.Email.objects.create(email=mailer_person.email, person=person)
    person.primary_email_address = email
    person.save()
    _save_mailing_preferences(email, mailer_person)
    _save_postal_address(person, mailer_person)


def _save_postal_address(person: models.Person, mailer_person: MailerPerson):
    address = models.Postal(
        person=person,
        country=mailer_person.country,
        address=mailer_person.address,
        postcode=mailer_person.postcode,
        city=mailer_person.city,
    )
    address.save()
    person.primary_postal_address = address
    person.save()


def _save_mailing_preferences(email: models.Email, mailer_person: MailerPerson):
    mailing_preferences, _ = MailingPreferences.objects.get_or_create(email=email)
    mailing_preferences.status = mailer_person.status
    mailing_preferences.interests.clear()
    for interest_id in mailer_person.interests_ids:
        interest = Interest.objects.get(external_id=interest_id)
        mailing_preferences.interests.add(interest)
    mailing_preferences.save()
