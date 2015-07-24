# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import whats_fresh.whats_fresh_api.models


class Migration(migrations.Migration):

    dependencies = [
        ('whats_fresh_api', '0003_auto_20141121_1945'),
    ]

    operations = [
        migrations.CreateModel(
            name='Theme',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False,
                                        auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=50)),
                ('background_color',
                 whats_fresh.whats_fresh_api.models.ColorField(max_length=10,
                                                               blank=True)),
                ('foreground_color',
                 whats_fresh.whats_fresh_api.models.ColorField(max_length=10,
                                                               blank=True)),
                ('logo', models.ImageField(upload_to=b'images')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
