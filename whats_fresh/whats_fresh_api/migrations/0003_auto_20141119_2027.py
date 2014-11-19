# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('whats_fresh_api', '0002_auto_20141119_0022'),
    ]

    operations = [
        migrations.AddField(
            model_name='image',
            name='name',
            field=models.TextField(default=b'Name'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='video',
            name='name',
            field=models.TextField(default=b'Name'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='story',
            name='buying',
            field=models.TextField(blank=True),
        ),
        migrations.AlterField(
            model_name='story',
            name='facts',
            field=models.TextField(blank=True),
        ),
        migrations.AlterField(
            model_name='story',
            name='history',
            field=models.TextField(blank=True),
        ),
        migrations.AlterField(
            model_name='story',
            name='images',
            field=models.ManyToManyField(to=b'whats_fresh_api.Image', null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='story',
            name='preparing',
            field=models.TextField(blank=True),
        ),
        migrations.AlterField(
            model_name='story',
            name='products',
            field=models.TextField(blank=True),
        ),
        migrations.AlterField(
            model_name='story',
            name='season',
            field=models.TextField(blank=True),
        ),
        migrations.AlterField(
            model_name='story',
            name='videos',
            field=models.ManyToManyField(to=b'whats_fresh_api.Video', null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='vendor',
            name='story',
            field=models.ForeignKey(blank=True, to='whats_fresh_api.Story', null=True),
        ),
    ]
