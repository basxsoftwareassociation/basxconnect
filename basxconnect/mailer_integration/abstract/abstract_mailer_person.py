import abc
import typing


class MailerPerson(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def first_name(self) -> str:
        pass

    @abc.abstractmethod
    def last_name(self) -> str:
        pass

    @abc.abstractmethod
    def display_name(self) -> str:
        pass

    @abc.abstractmethod
    def email(self) -> str:
        pass

    @abc.abstractmethod
    def interests_ids(self) -> typing.List[str]:
        pass

    @abc.abstractmethod
    def status(self) -> str:
        pass

    def country(person):
        pass

    def postcode(person):
        pass

    def address(person):
        pass

    def city(person):
        pass
