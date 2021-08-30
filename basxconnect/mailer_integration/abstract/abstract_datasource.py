import abc
from typing import List, NamedTuple

from basxconnect.mailer_integration.models import MailingPreferences


class MailerPerson(NamedTuple):
    display_name: str
    email: str
    interests_ids: List[str]
    status: str
    last_name: str = ""
    first_name: str = ""
    country: str = ""  # in alpha_2 format (e.g. "CH", "DE", ...)
    postcode: str = ""
    address: str = ""
    city: str = ""

    @staticmethod
    def from_mailing_preferences(preferences: MailingPreferences):
        person = preferences.email.person
        return MailerPerson(
            display_name=person.name,
            first_name=(
                person.naturalperson.first_name
                if hasattr(person, "naturalperson")
                else ""
            ),
            last_name=(
                person.naturalperson.last_name
                if hasattr(person, "naturalperson")
                else ""
            ),
            email=preferences.email.email,
            interests_ids=[
                interest.external_id for interest in preferences.interests.all()
            ],
            status=preferences.status,
        )


class MailingInterest(NamedTuple):
    id: str
    name: str


class Datasource(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def get_persons(self) -> List[MailerPerson]:
        pass

    @abc.abstractmethod
    def put_person(self, person: MailerPerson):
        pass

    @abc.abstractmethod
    def get_interests(self) -> List[MailingInterest]:
        pass

    @abc.abstractmethod
    def tag(
        self,
    ) -> str:
        pass
