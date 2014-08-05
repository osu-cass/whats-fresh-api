from django.contrib.gis.db import models
import os
from phonenumber_field.modelfields import PhoneNumberField

class Image(models.Model):
    """
    The Image model holds an image and related data.

    The Created and Modified time fields are created automatically by
    Django when the object is created or modified, and can not be altered.

    This model uses Django's built-ins for holding the image location and
    data in the database, as well as for keeping created and modified
    timestamps.
    """

    image = models.ImageField(upload_to='%Y/%m/%d')
    caption = models.TextField()

    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)


class Vendor(models.Model):
    """
    The Vendor model holds the information for a vendor, including the
    geographic location as a pair of latitudinal/logitudinal coordinates,
    a street address, and an optional text description of their location
    (in case the address/coordinates are of, say, a dock instead of a shop).
    """
    pass


class Product(models.Model):
    """
    The Product model holds the information for a product, including the
    origin, season, market price, and availability.

    In addition, it holds a foreign key to the image and story related to the
    product.
    """
    name = models.TextField()
    variety = models.TextField()
    alt_name = models.TextField()
    description = models.TextField()
    origin = models.TextField()

    season = models.TextField()
    available = models.NullBooleanField()
    market_price = models.TextField()
    link = models.URLField()

    image_id = models.ForeignKey('Image')
    story_id = models.ForeignKey('Story')

    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)


class Story(models.Model):
    """
    The story model holds the stories for products and vendors
    """
    pass
