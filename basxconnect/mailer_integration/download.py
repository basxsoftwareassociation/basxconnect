from typing import Any, NamedTuple

import basxconnect
from basxconnect.core import models
from basxconnect.mailer_integration.abstract.abstract_datasource import Datasource
from basxconnect.mailer_integration.models import Interest, MailingPreferences


class SynchronizationResult(NamedTuple):
    new_persons: int
    total_synchronized_persons: int


def download_persons(datasource: Datasource) -> SynchronizationResult:
    MailingPreferences.objects.all().delete()
    Interest.objects.all().delete()

    raw_persons = datasource.get_persons()
    reader = datasource.person_reader()
    datasource_tag = _get_or_create_tag(datasource.tag())
    new_persons = 0
    for raw_person in raw_persons:
        matching_persons = list(
            models.Person.objects.filter(
                primary_email_address__email=reader.email_of(raw_person), deleted=False
            ).all()
        )
        if len(matching_persons) == 0:
            _save_person(datasource_tag, raw_person, reader)
            new_persons += 1
        else:
            # if the downloaded email address already exists in our system, update the mailing preference of all persons
            # that use this email address (as primary email address), without creating a new person in the database
            for person in matching_persons:
                _save_mailing_preferences(person, raw_person, reader)

    return SynchronizationResult(new_persons, len(raw_persons))


def _is_new_person(
    person: Any,
    reader: basxconnect.mailer_integration.abstract.abstract_person_reader.PersonReader,
) -> bool:
    return not models.Person.objects.filter(
        primary_email_address__email=reader.email_of(person), deleted=False
    ).exists()


def _get_or_create_tag(tag: str) -> models.Term:
    tags_category_id = models.Category.objects.get(slug="category").id
    if not models.Term.objects.filter(term=tag, category_id=tags_category_id).exists():
        models.Term(term=tag, category_id=tags_category_id).save()
    return models.Term.objects.get(term=tag, category_id=tags_category_id)


def _save_person(datasource_tag, raw_person, reader):
    person = models.NaturalPerson(
        first_name=reader.first_name_of(raw_person),
        name=reader.display_name_of(raw_person),
        last_name=reader.last_name_of(raw_person),
    )
    person.save()
    email = models.Email(email=reader.email_of(raw_person), person=person)
    email.save()
    person.primary_email_address = email
    person.categories.add(datasource_tag)
    person.save()
    _save_mailing_preferences(person, raw_person, reader)


def _save_mailing_preferences(person, raw_person, reader):
    try:
        mailing_preferences = MailingPreferences.objects.get(person=person)
    except MailingPreferences.DoesNotExist:
        mailing_preferences = MailingPreferences(
            person=person, status=reader.status_of(raw_person)
        )
        mailing_preferences.save()
    mailing_preferences.status = reader.status_of(raw_person)
    mailing_preferences.interests.clear()
    for raw_interest in reader.interests_of(raw_person):
        interest = _get_or_create_interest(raw_interest)
        mailing_preferences.interests.add(interest)
    mailing_preferences.save()


def _get_or_create_interest(interest: str) -> models.Term:
    try:
        interest = Interest.objects.get(name=interest)
    except Interest.DoesNotExist:
        interest = Interest(name=interest)
        interest.save()
    return interest
