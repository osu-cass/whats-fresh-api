# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('whats_fresh_api', '0004_theme'),
    ]

    operations = [
        migrations.AddField(
            model_name='theme',
            name='images',
            field=models.CharField(
                default=b'images', unique=True, max_length=100),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='theme',
            name='images_slug',
            field=models.SlugField(
                default=b'images', unique=True, max_length=40),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='theme',
            name='preparations',
            field=models.CharField(
                default=b'preparations', unique=True, max_length=100),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='theme',
            name='preparations_slug',
            field=models.SlugField(
                default=b'preparations', unique=True, max_length=40),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='theme',
            name='products',
            field=models.CharField(
                default=b'products', unique=True, max_length=100),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='theme',
            name='products_slug',
            field=models.SlugField(
                default=b'products', unique=True, max_length=40),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='theme',
            name='site_name',
            field=models.CharField(
                default=b"Oregon's Catch", unique=True, max_length=50),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='theme',
            name='site_name_slug',
            field=models.SlugField(
                default=b"Oregon's Catch", unique=True, max_length=40),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='theme',
            name='stories',
            field=models.CharField(
                default=b'stories', unique=True, max_length=100),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='theme',
            name='stories_slug',
            field=models.SlugField(
                default=b'stories', unique=True, max_length=40),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='theme',
            name='vendors',
            field=models.CharField(
                default=b'vendors', unique=True, max_length=100),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='theme',
            name='vendors_slug',
            field=models.SlugField(
                default=b'vendors', unique=True, max_length=40),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='theme',
            name='videos',
            field=models.CharField(
                default=b'videos', unique=True, max_length=100),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='theme',
            name='videos_slug',
            field=models.SlugField(
                default=b'videos', unique=True, max_length=40),
            preserve_default=True,
        ),
    ]
