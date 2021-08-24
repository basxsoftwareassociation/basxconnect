import abc
from typing import List, NamedTuple

from basxconnect.mailer_integration.abstract.abstract_mailer_person import MailerPerson


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
