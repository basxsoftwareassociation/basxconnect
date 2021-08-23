from typing import NamedTuple

from basxconnect.core import models
from basxconnect.mailer_integration.abstract.abstract_datasource import Datasource
from basxconnect.mailer_integration.abstract.abstract_mailer_person import MailerPerson
from basxconnect.mailer_integration.models import Interest, MailingPreferences


class SynchronizationResult(NamedTuple):
    new_persons: int
    total_synchronized_persons: int


def download_persons(datasource: Datasource) -> SynchronizationResult:
    mailer_persons = datasource.get_persons()
    datasource_tag = _get_or_create_tag(datasource.tag())
    new_persons = 0
    for mailer_person in mailer_persons:
        matching_persons = list(
            models.Person.objects.filter(
                primary_email_address__email=mailer_person.email(), deleted=False
            ).all()
        )
        if len(matching_persons) == 0:
            _save_person(datasource_tag, mailer_person)
            new_persons += 1
        else:
            # if the downloaded email address already exists in our system, update the mailing preference of all persons
            # that use this email address (as primary email address), without creating a new person in the database
            for person in matching_persons:
                _save_mailing_preferences(person, mailer_person)

    return SynchronizationResult(new_persons, len(mailer_persons))


def _is_new_person(
    person: MailerPerson,
) -> bool:
    return not models.Person.objects.filter(
        primary_email_address__email=person.email(), deleted=False
    ).exists()


def _get_or_create_tag(tag: str) -> models.Term:
    tags_category = models.Category.objects.get(slug="category")
    tag, _ = models.Term.objects.get_or_create(term=tag, category_id=tags_category)
    return tag


def _save_person(datasource_tag, mailer_person):
    person = models.NaturalPerson.objects.create(
        first_name=mailer_person.first_name(),
        name=mailer_person.display_name(),
        last_name=mailer_person.last_name(),
    )
    email = models.Email.objects.create(email=mailer_person.email(), person=person)
    person.primary_email_address = email
    person.categories.add(datasource_tag)
    person.save()
    _save_mailing_preferences(person, mailer_person)


def _save_mailing_preferences(person, mailer_person):
    mailing_preferences, _ = MailingPreferences.objects.get_or_create(person=person)
    mailing_preferences.status = mailer_person.status()
    mailing_preferences.interests.clear()
    for raw_interest in mailer_person.interests():
        interest, _ = Interest.objects.get_or_create(name=raw_interest)
        mailing_preferences.interests.add(interest)
    mailing_preferences.save()
