# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('whats_fresh_api', '0003_auto_20141121_1945'),
    ]

    operations = [
        migrations.CreateModel(
            name='Theme',
            fields=[
                ('id', models.AutoField(
                    verbose_name='ID', serialize=False, auto_created=True,
                    primary_key=True)),
                ('name', models.CharField(unique=True, max_length=50)),
                ('background_color', models.TextField(
                    default=b'rgb(81, 114, 133)', max_length=50)),
                ('foreground_color', models.TextField(
                    default=b'rgb(81, 114, 133)', max_length=50)),
                ('header_color', models.TextField(
                    default=b'rgb(255, 255, 255)', max_length=50)),
                ('font_color', models.TextField(
                    default=b'rgb(51, 51, 51)', max_length=50)),
                ('logo', models.ImageField(
                    null=True, upload_to=b'images', blank=True)),
                ('slogan', models.CharField(
                    max_length=50, null=True, blank=True)),
                ('site_title', models.CharField(
                    default=b"Oregon's Catch", max_length=50)),
                ('vendors', models.CharField(
                    default=b'Vendors', max_length=100)),
                ('vendors_slug', models.SlugField(
                    default=b'vendors', max_length=40)),
                ('products', models.CharField(
                    default=b'Products', max_length=100)),
                ('products_slug', models.SlugField(
                    default=b'products', max_length=40)),
                ('preparations', models.CharField(
                    default=b'Preparations', max_length=100)),
                ('preparations_slug', models.SlugField(
                    default=b'preparations', max_length=40)),
                ('stories', models.CharField(
                    default=b'Stories', max_length=100)),
                ('stories_slug', models.SlugField(
                    default=b'stories', max_length=40)),
                ('videos', models.CharField(
                    default=b'Videos', max_length=100)),
                ('videos_slug', models.SlugField(
                    default=b'videos', max_length=40)),
                ('images', models.CharField(
                    default=b'Images', max_length=100)),
                ('images_slug', models.SlugField(
                    default=b'images', max_length=40)),
                ('active', models.CharField(
                    default=b'No', max_length=5,
                    choices=[(b'Yes', b'Yes'), (b'No', b'No')])),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
