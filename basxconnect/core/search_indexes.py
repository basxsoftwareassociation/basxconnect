from celery_haystack.indexes import CelerySearchIndex
from haystack import indexes

from . import models


class PersonIndex(CelerySearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, model_attr="name")
    name_auto = indexes.EdgeNgramField(model_attr="name")

    def get_model(self):
        return models.Person


class NaturalPersonIndex(PersonIndex):
    def get_model(self):
        return models.NaturalPerson


class LegalPersonIndex(PersonIndex):
    def get_model(self):
        return models.LegalPerson


class PersonAssociationIndex(PersonIndex):
    def get_model(self):
        return models.PersonAssociation
