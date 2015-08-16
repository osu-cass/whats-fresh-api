from haystack import indexes
from .models import Vendor, Product


class VendorIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    name = indexes.CharField(model_attr='name')
    # content_auto = indexes.EdgeNgramField(model_attr='name')

    def get_model(self):
        return Vendor

    def index_queryset(self, using=None):
        return self.get_model().objects.all()


class ProductIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    name = indexes.CharField(model_attr='name')
    # content_auto = indexes.EdgeNgramField(model_attr='name')

    def get_model(self):
        return Product

    def index_queryset(self, using=None):
        return self.get_model().objects.all()

