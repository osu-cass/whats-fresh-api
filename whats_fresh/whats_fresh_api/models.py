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
    def filename(self):
        return os.path.basename(self.image.name)

    def __unicode__(self):
        return self.filename()

    image = models.ImageField(upload_to='images')
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
    def __unicode__(self):
        return self.name

    name = models.TextField()
    description = models.TextField()
    status = models.NullBooleanField()

    street = models.TextField()
    city = models.TextField()
    state = models.TextField()
    zip = models.TextField()
    location_description = models.TextField()

    contact_name = models.TextField()
    website = models.URLField()
    email = models.EmailField()
    phone = PhoneNumberField()

    lat = models.FloatField()
    long = models.FloatField()

    story_id = models.ForeignKey('Story')
    products = models.ManyToManyField(
        'Product',
        related_name='vendors',
        through='VendorProduct')

    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)


class Product(models.Model):
    """
    The Product model holds the information for a product, including the
    origin, season, market price, and availability.

    In addition, it holds a foreign key to the image and story related to the
    product.
    """
    def __unicode__(self):
        return self.name

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

    preparations = models.ManyToManyField(
        'Preparation', related_name='products', through='ProductPreparation')

    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)


class Story(models.Model):
    """
    The story model holds the stories for products and vendors
    """
    def __unicode__(self):
        if not self.id:
            return u'Unsaved story'
        else:
            return u'Story %d' % self.id

    story = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)


class Preparation(models.Model):
    """
    The Preparation model contains possible preparations of product, to be
    associated many-to-many with product (a product can have one or more
    preparations, preparations apply to many products). Preparations may be
    things like 'frozen', 'dried', 'fresh', 'live', etc, to be defined by
    Sea Grant data input.
    """
    def __unicode__(self):
        return self.name

    name = models.TextField()
    description = models.TextField()
    additional_info = models.TextField()


class ProductPreparation(models.Model):
    """
    The Product Preparation model contains the relationship of products and
    preparations.
    """
    def __unicode__(self):
        if not self.product:
            return "Unsaved product/preparation join"
        else:
            return "Preparations for product %s" % (self.product.name)

    product = models.ForeignKey(Product, null=True)
    preparation = models.ForeignKey(Preparation)


class VendorProduct(models.Model):
    """
    Keep track of the products each vendor has.

    The ForeignKey vendor field here means this creates a one-to-many -- each
    vendor can have many VendorProducts, but a VendorProduct can only have one
    vendor. In the same way, each VendorProduct can only have one product and
    one preparation.
    """
    def __unicode__(self):
        if not self.vendor:
            return "Unsaved product/vendor join"
        else:
            return "Products for vendor %s" % (self.vendor.name)

    vendor = models.ForeignKey(Vendor, null=True)
    product = models.ForeignKey(Product)
    preparation = models.ForeignKey(Preparation)

    vendor_price = models.TextField()
    available = models.NullBooleanField()
