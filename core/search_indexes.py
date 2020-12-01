from haystack import indexes

from celery_haystack.indexes import CelerySearchIndex

from . import models


class PersonIndex(CelerySearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, model_attr="name")
    name_auto = indexes.EdgeNgramField(model_attr="name")

    def get_model(self):
        return models.Person


class NaturalPersonIndex(PersonIndex):
    def get_model(self):
        return models.NaturalPerson


class JuristicPersonIndex(PersonIndex):
    def get_model(self):
        return models.JuristicPerson


class PersonAssociationIndex(PersonIndex):
    def get_model(self):
        return models.PersonAssociation
