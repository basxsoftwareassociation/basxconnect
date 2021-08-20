import abc
from typing import List

from basxconnect.mailer_integration.abstract.abstract_mailer_person import MailerPerson


class Datasource(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def get_persons(self) -> List[MailerPerson]:
        pass

    @abc.abstractmethod
    def tag(
        self,
    ) -> str:
        pass
