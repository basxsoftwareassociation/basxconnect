from celery_haystack.indexes import CelerySearchIndex
from haystack import indexes

from . import models


class PersonIndex(CelerySearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, model_attr="search_index_snippet")
    personnumber = indexes.IntegerField(model_attr="personnumber")
    name_auto = indexes.EdgeNgramField(model_attr="search_index_snippet")

    def get_model(self):
        return models.Person
