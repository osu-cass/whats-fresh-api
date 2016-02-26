from django.contrib.gis.db import models
import os
from phonenumber_field.modelfields import PhoneNumberField
import whats_fresh.whats_fresh_api.signals  # noqa


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
        return self.name

    image = models.ImageField(upload_to='images')
    name = models.TextField(default='')
    caption = models.TextField(blank=True)

    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    def natural_key(self):
        return {
            'name': self.name,
            'caption': self.caption,
            'link': self.image.url
        }


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

    hours = models.TextField(blank=True)

    street = models.TextField()
    city = models.TextField()
    state = models.TextField()
    zip = models.TextField()
    location_description = models.TextField(blank=True)
    status = models.NullBooleanField()

    contact_name = models.TextField()
    website = models.URLField(blank=True)
    email = models.EmailField(blank=True)
    phone = PhoneNumberField(blank=True, null=True)

    # Geo Django field to store a point
    location = models.PointField()
    objects = models.GeoManager()

    story = models.ForeignKey('Story', null=True, blank=True)
    products_preparations = models.ManyToManyField(
        'ProductPreparation',
        related_name='vendors',
        through='VendorProduct',
        blank=True)

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
    variety = models.TextField(blank=True)
    alt_name = models.TextField(blank=True)
    description = models.TextField()
    origin = models.TextField(blank=True)

    season = models.TextField()
    available = models.NullBooleanField()
    market_price = models.TextField()
    link = models.URLField(blank=True)

    image = models.ForeignKey('Image', null=True, blank=True)
    story = models.ForeignKey('Story', null=True, blank=True)

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
            return self.name

    name = models.TextField()
    history = models.TextField(blank=True)
    facts = models.TextField(blank=True)
    buying = models.TextField(blank=True)
    preparing = models.TextField(blank=True)
    products = models.TextField(blank=True)
    season = models.TextField(blank=True)
    images = models.ManyToManyField('Image', null=True, blank=True)
    videos = models.ManyToManyField('Video', null=True, blank=True)
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
    description = models.TextField(blank=True)
    additional_info = models.TextField(blank=True)


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

    product = models.ForeignKey(Product)
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

    vendor = models.ForeignKey(Vendor)
    product_preparation = models.ForeignKey(ProductPreparation)

    vendor_price = models.TextField(blank=True)
    available = models.NullBooleanField()


class Video(models.Model):

    """
    The video model holds a video URL and related data.

    The Created and Modified time fields are created automatically by
    Django when the object is created or modified, and can not be altered.

    This model uses Django's built-ins for holding the video URL and
    data in the database, as well as for keeping created and modified
    timestamps.
    """

    def __unicode__(self):
        return self.caption

    video = models.URLField()
    caption = models.TextField(blank=True)
    name = models.TextField(default='')

    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    def natural_key(self):
        return {
            'caption': self.caption,
            'name': self.name,
            'link': self.video
        }


class Theme(models.Model):

    """
    The themes model holds theming and customiztion data.

    The user will be able to define his own customization for the site
    in the form of personel color prepferences, site logo etc.
    """

    def __unicode__(self):
        return self.name

    CHOICES = (
        ('Yes', 'Yes'),
        ('No', 'No'),
    )

    name = models.CharField(max_length=50, unique=True)
    background_color = models.TextField(
        max_length=50, default="rgb(81, 114, 133)")
    foreground_color = models.TextField(
        max_length=50, default="rgb(81, 114, 133)")
    header_color = models.TextField(
        max_length=50, default="rgb(255, 255, 255)")
    font_color = models.TextField(max_length=50, default="rgb(51, 51, 51)")
    logo = models.ImageField(upload_to='images', null=True, blank=True)
    slogan = models.CharField(max_length=50, null=True, blank=True)
    site_title = models.CharField(max_length=50, default="Oregon's Catch")
    vendors = models.CharField(max_length=100, default="Vendors")
    vendors_slug = models.SlugField(max_length=40, default="vendors")
    products = models.CharField(max_length=100, default="Products")
    products_slug = models.SlugField(max_length=40, default="products")
    preparations = models.CharField(max_length=100, default="Preparations")
    preparations_slug = models.SlugField(max_length=40, default="preparations")
    stories = models.CharField(max_length=100, default="Stories")
    stories_slug = models.SlugField(max_length=40, default="stories")
    videos = models.CharField(max_length=100, default="Videos")
    videos_slug = models.SlugField(max_length=40, default="videos")
    images = models.CharField(max_length=100, default="Images")
    images_slug = models.SlugField(max_length=40, default="images")
    active = models.CharField(max_length=5, choices=CHOICES, default="No")

    def save(self, *args, **kwargs):
        if self.active == "Yes":
            try:
                temp = Theme.objects.get(active="Yes")
                if self != temp:
                    temp.active = "No"
                    temp.save()
            except Theme.DoesNotExist:
                pass
        super(Theme, self).save(*args, **kwargs)
