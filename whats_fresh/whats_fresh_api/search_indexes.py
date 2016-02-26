from haystack import indexes
from whats_fresh.whats_fresh_api.models import (
    Vendor, Product, Preparation, Story, Image, Video)


class VendorIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    content_auto = indexes.EdgeNgramField(model_attr='name')

    def get_model(self):
        return Vendor

    def index_queryset(self, using=None):
        return self.get_model().objects.all()


class ProductIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    content_auto = indexes.EdgeNgramField(model_attr='name')

    def get_model(self):
        return Product

    def index_queryset(self, using=None):
        return self.get_model().objects.all()


class PreparationIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    content_auto = indexes.EdgeNgramField(model_attr='name')

    def get_model(self):
        return Preparation

    def index_queryset(self, using=None):
        return self.get_model().objects.all()


class StoryIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    content_auto = indexes.EdgeNgramField(model_attr='name')

    def get_model(self):
        return Story

    def index_queryset(self, using=None):
        return self.get_model().objects.all()


class ImageIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    content_auto = indexes.EdgeNgramField(model_attr='name')

    def get_model(self):
        return Image

    def index_queryset(self, using=None):
        return self.get_model().objects.all()


class VideoIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    content_auto = indexes.EdgeNgramField(model_attr='name')

    def get_model(self):
        return Video

    def index_queryset(self, using=None):
        return self.get_model().objects.all()
