import django_countries
from django.utils import timezone

from basxconnect.core import models
from basxconnect.mailer_integration.abstract.abstract_datasource import (
    Datasource,
    MailerPerson,
)
from basxconnect.mailer_integration.models import (
    Interest,
    Subscription,
    SynchronizationPerson,
    SynchronizationResult,
)


def synchronize(datasource: Datasource) -> SynchronizationResult:
    synchronize_interests(datasource)

    mailer_persons = datasource.get_persons()
    datasource_tag = _get_or_create_tag(datasource.tag())
    sync_result = SynchronizationResult.objects.create()
    for mailer_person in mailer_persons:
        matching_email_addresses = list(
            models.Email.objects.filter(
                email=mailer_person.email,
            ).all()
        )
        if len(matching_email_addresses) == 0:
            if not is_valid_new_person(mailer_person):
                _save_sync_person(
                    mailer_person, sync_result, SynchronizationPerson.SKIPPED
                )
            else:
                created_person = _save_person(datasource_tag, mailer_person)
                _save_subscription(
                    created_person.primary_email_address, mailer_person, sync_result
                )
                _save_sync_person(mailer_person, sync_result, SynchronizationPerson.NEW)
        else:
            # if the downloaded email address already exists in our system, update the mailing preference for this email
            # address, without creating a new person in the database
            for email in matching_email_addresses:
                _save_subscription(email, mailer_person, sync_result)
    sync_result.total_synchronized_persons = len(mailer_persons)
    sync_result.sync_completed_datetime = timezone.now()
    sync_result.save()

    return sync_result


def synchronize_interests(datasource):
    old_interests = Interest.objects.all()
    downloaded_interests = datasource.get_interests()
    new_interests_ids = []
    for interest in downloaded_interests:
        interest_from_db, _ = Interest.objects.get_or_create(
            external_id=interest.id, name=interest.name
        )
        new_interests_ids.append(interest_from_db.id)
    for interest in old_interests:
        if interest.id not in new_interests_ids:
            interest.delete()


def _get_or_create_tag(tag: str) -> models.Term:
    tags_vocabulary = models.Vocabulary.objects.get(slug="tag")
    tag, _ = models.Term.objects.get_or_create(term=tag, vocabulary=tags_vocabulary)
    return tag


def is_valid_new_person(person: MailerPerson):
    return django_countries.Countries().countries.get(
        person.country
    ) and person.status in ["subscribed", "unsubscribed", "cleaned"]


def _save_sync_person(mailer_person, sync_result, syn_status):
    SynchronizationPerson.objects.create(
        sync_result=sync_result,
        email=mailer_person.email,
        first_name=mailer_person.first_name,
        last_name=mailer_person.last_name,
        sync_status=syn_status,
    )


def _save_person(datasource_tag: models.Term, mailer_person: MailerPerson):
    person = models.NaturalPerson.objects.create(
        first_name=mailer_person.first_name,
        name=mailer_person.display_name,
        last_name=mailer_person.last_name,
    )
    person.tags.add(datasource_tag)
    person.save()
    email = models.Email.objects.create(email=mailer_person.email, person=person)
    person.primary_email_address = email
    person.save()
    _save_postal_address(person, mailer_person)
    return person


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


def _save_subscription(
    email: models.Email, mailer_person: MailerPerson, sync_result: SynchronizationResult
):
    mailing_preferences, _ = Subscription.objects.get_or_create(email=email)
    mailing_preferences.status = mailer_person.status
    mailing_preferences.language = mailer_person.language
    mailing_preferences.interests.clear()
    for interest_id in mailer_person.interests_ids:
        interest = Interest.objects.get(external_id=interest_id)
        mailing_preferences.interests.add(interest)
    mailing_preferences.latest_sync = sync_result
    mailing_preferences.save()
