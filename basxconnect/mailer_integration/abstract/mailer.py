import abc
from typing import List, NamedTuple

from basxconnect.mailer_integration.models import Subscription


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
    language: str = ""

    @staticmethod
    def from_mailing_preferences(preferences: Subscription):
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
            language=preferences.language,
        )


class MailingInterest(NamedTuple):
    id: str
    name: str


class AbstractMailer(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def name(self) -> str:
        pass

    @abc.abstractmethod
    def get_person_count(self) -> int:
        pass

    @abc.abstractmethod
    def get_persons(
        self,
        count: int,
        offset: int,
    ) -> List[MailerPerson]:
        pass

    @abc.abstractmethod
    def put_person(self, person: MailerPerson, **kwargs):
        pass

    @abc.abstractmethod
    def add_person(self, person: MailerPerson):
        pass

    @abc.abstractmethod
    def email_exists(self, email: str) -> bool:
        pass

    @abc.abstractmethod
    def change_email_address(self, old_email: str, new_email: str):
        pass

    @abc.abstractmethod
    def get_interests(self) -> List[MailingInterest]:
        pass

    @abc.abstractmethod
    def tag(
        self,
    ) -> str:
        pass
