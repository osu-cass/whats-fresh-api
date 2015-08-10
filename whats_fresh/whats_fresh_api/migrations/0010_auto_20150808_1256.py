# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('whats_fresh_api', '0009_auto_20150808_1113'),
    ]

    operations = [
        migrations.AlterField(
            model_name='theme',
            name='logo',
            field=models.ImageField(
                null=True, upload_to=b'images', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='theme',
            name='slogan',
            field=models.CharField(max_length=50, null=True, blank=True),
            preserve_default=True,
        ),
    ]
