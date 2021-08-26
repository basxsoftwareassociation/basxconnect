import abc
from typing import List, NamedTuple

from basxconnect.core import models


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
    def from_email(email: models.Email):
        return MailerPerson(
            display_name=email.person.name,
            email=email.email,
            interests_ids=[
                interest.external_id
                for interest in email.mailingpreferences.interests.all()
            ],
            status=email.mailingpreferences.status,
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
    def post_person(self, person: MailerPerson):
        pass

    @abc.abstractmethod
    def get_interests(self) -> List[MailingInterest]:
        pass

    @abc.abstractmethod
    def tag(
        self,
    ) -> str:
        pass
