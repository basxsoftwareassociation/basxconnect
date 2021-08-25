import abc
from typing import List, NamedTuple


class MailerPerson(NamedTuple):
    first_name: str
    last_name: str
    display_name: str
    email: str
    interests_ids: List[str]
    status: str
    country: str
    postcode: str
    address: str
    city: str


class MailingInterest(NamedTuple):
    id: str
    name: str


class Datasource(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def get_persons(self) -> List[MailerPerson]:
        pass

    @abc.abstractmethod
    def get_interests(self) -> List[MailingInterest]:
        pass

    @abc.abstractmethod
    def tag(
        self,
    ) -> str:
        pass
