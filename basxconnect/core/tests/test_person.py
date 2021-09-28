from bread.tests.helper import generic_bread_testcase
from hypothesis.extra.django import from_model

from basxconnect.core import models


class VocabularyTest(generic_bread_testcase(models.Vocabulary)):
    pass


class TermTest(
    generic_bread_testcase(models.Term, vocabulary=from_model(models.Vocabulary))
):
    pass


class PersonTest(generic_bread_testcase(models.Person)):
    pass


class NaturalPersonTest(generic_bread_testcase(models.NaturalPerson)):
    pass


class LegalPersonTest(generic_bread_testcase(models.LegalPerson)):
    pass


class PersonAssociationTest(generic_bread_testcase(models.PersonAssociation)):
    pass
