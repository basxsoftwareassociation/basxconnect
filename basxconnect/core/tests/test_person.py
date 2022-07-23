from basxbread.tests.helper import generic_basxbread_testcase
from hypothesis.extra.django import from_model

from basxconnect.core import models


class VocabularyTest(generic_basxbread_testcase(models.Vocabulary)):
    pass


class TermTest(
    generic_basxbread_testcase(models.Term, vocabulary=from_model(models.Vocabulary))
):
    pass


class PersonTest(generic_basxbread_testcase(models.Person)):
    pass


class NaturalPersonTest(generic_basxbread_testcase(models.NaturalPerson)):
    pass


class LegalPersonTest(generic_basxbread_testcase(models.LegalPerson)):
    pass


class PersonAssociationTest(generic_basxbread_testcase(models.PersonAssociation)):
    pass
