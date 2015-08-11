# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('whats_fresh_api', '0010_auto_20150808_1256'),
    ]

    operations = [
        migrations.AlterField(
            model_name='theme',
            name='active',
            field=models.CharField(default=b'No', max_length=5, choices=[(b'Yes', b'Yes'), (b'No', b'No')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='theme',
            name='images',
            field=models.CharField(default=b'images', max_length=100),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='theme',
            name='images_slug',
            field=models.SlugField(default=b'images', max_length=40),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='theme',
            name='preparations',
            field=models.CharField(default=b'preparations', max_length=100),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='theme',
            name='preparations_slug',
            field=models.SlugField(default=b'preparations', max_length=40),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='theme',
            name='products',
            field=models.CharField(default=b'products', max_length=100),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='theme',
            name='products_slug',
            field=models.SlugField(default=b'products', max_length=40),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='theme',
            name='site_title',
            field=models.CharField(default=b"Oregon's Catch", max_length=50),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='theme',
            name='stories',
            field=models.CharField(default=b'stories', max_length=100),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='theme',
            name='stories_slug',
            field=models.SlugField(default=b'stories', max_length=40),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='theme',
            name='vendors',
            field=models.CharField(default=b'vendors', max_length=100),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='theme',
            name='vendors_slug',
            field=models.SlugField(default=b'vendors', max_length=40),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='theme',
            name='videos',
            field=models.CharField(default=b'videos', max_length=100),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='theme',
            name='videos_slug',
            field=models.SlugField(default=b'videos', max_length=40),
            preserve_default=True,
        ),
    ]
