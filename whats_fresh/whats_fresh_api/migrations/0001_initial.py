# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import phonenumber_field.modelfields
import django.contrib.gis.db.models.fields


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Image',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('image', models.ImageField(upload_to=b'images')),
                ('name', models.TextField()),
                ('caption', models.TextField(blank=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Preparation',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.TextField()),
                ('description', models.TextField(blank=True)),
                ('additional_info', models.TextField(blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.TextField()),
                ('variety', models.TextField(blank=True)),
                ('alt_name', models.TextField(blank=True)),
                ('description', models.TextField()),
                ('origin', models.TextField(blank=True)),
                ('season', models.TextField()),
                ('available', models.NullBooleanField()),
                ('market_price', models.TextField()),
                ('link', models.URLField(blank=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('image', models.ForeignKey(blank=True, to='whats_fresh_api.Image', null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ProductPreparation',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('preparation', models.ForeignKey(to='whats_fresh_api.Preparation')),
                ('product', models.ForeignKey(to='whats_fresh_api.Product')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Story',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.TextField()),
                ('history', models.TextField(blank=True)),
                ('facts', models.TextField(blank=True)),
                ('buying', models.TextField(blank=True)),
                ('preparing', models.TextField(blank=True)),
                ('products', models.TextField(blank=True)),
                ('season', models.TextField(blank=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('images', models.ManyToManyField(to='whats_fresh_api.Image', null=True, blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Vendor',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.TextField()),
                ('description', models.TextField()),
                ('hours', models.TextField(blank=True)),
                ('street', models.TextField()),
                ('city', models.TextField()),
                ('state', models.TextField()),
                ('zip', models.TextField()),
                ('location_description', models.TextField(blank=True)),
                ('status', models.NullBooleanField()),
                ('contact_name', models.TextField()),
                ('website', models.URLField(blank=True)),
                ('email', models.EmailField(max_length=75, blank=True)),
                ('phone', phonenumber_field.modelfields.PhoneNumberField(max_length=128, null=True, blank=True)),
                ('location', django.contrib.gis.db.models.fields.PointField(srid=4326)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='VendorProduct',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('vendor_price', models.TextField(blank=True)),
                ('available', models.NullBooleanField()),
                ('product_preparation', models.ForeignKey(to='whats_fresh_api.ProductPreparation')),
                ('vendor', models.ForeignKey(to='whats_fresh_api.Vendor')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Video',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('video', models.URLField()),
                ('caption', models.TextField(blank=True)),
                ('name', models.TextField()),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='vendor',
            name='products_preparations',
            field=models.ManyToManyField(related_name=b'vendors', through='whats_fresh_api.VendorProduct', to='whats_fresh_api.ProductPreparation', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='vendor',
            name='story',
            field=models.ForeignKey(blank=True, to='whats_fresh_api.Story', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='story',
            name='videos',
            field=models.ManyToManyField(to='whats_fresh_api.Video', null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='product',
            name='preparations',
            field=models.ManyToManyField(related_name=b'products', through='whats_fresh_api.ProductPreparation', to='whats_fresh_api.Preparation'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='product',
            name='story',
            field=models.ForeignKey(blank=True, to='whats_fresh_api.Story', null=True),
            preserve_default=True,
        ),
    ]
