from django.contrib.gis.db import models
import os

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


class Preparation(models.Model):
    """
    The Preparation model contains possible preparations of product, to be
    associated many-to-many with product (a product can have one or more
    preparations, preparations apply to many products). Preparations may be
    things like 'frozen', 'dried', 'fresh', 'live', etc, to be defined by
    Sea Grant data input.
    """
    pass
