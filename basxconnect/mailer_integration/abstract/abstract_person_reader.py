import abc
import typing


class PersonReader(metaclass=abc.ABCMeta):
    @staticmethod
    @abc.abstractmethod
    def first_name_of(person: typing.Any) -> str:
        pass

    @staticmethod
    @abc.abstractmethod
    def last_name_of(person: typing.Any) -> str:
        pass

    @staticmethod
    @abc.abstractmethod
    def display_name_of(person: typing.Any) -> str:
        pass

    @staticmethod
    @abc.abstractmethod
    def email_of(person: typing.Any) -> str:
        pass

    @staticmethod
    @abc.abstractmethod
    def interests_of(person: typing.Any) -> typing.List[str]:
        pass

    @staticmethod
    @abc.abstractmethod
    def status_of(person: typing.Any) -> str:
        pass
