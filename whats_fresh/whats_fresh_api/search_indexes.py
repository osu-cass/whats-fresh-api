from haystack import indexes
from .models import Vendor


class VendorIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    name = indexes.CharField(model_attr='name')

    def get_model(self):
        return Vendor

    def index_queryset(self, using=None):
        return self.get_model().objects.all()
