import abc
from typing import Any, List

from basxconnect.mailer_integration.abstract.abstract_person_reader import PersonReader


class Datasource(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def get_persons(self) -> List[Any]:
        pass

    @abc.abstractmethod
    def person_reader(
        self,
    ) -> PersonReader:
        pass

    @abc.abstractmethod
    def tag(
        self,
    ) -> str:
        pass
