# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('whats_fresh_api', '0008_auto_20150805_1958'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='theme',
            name='site_title_slug',
        ),
        migrations.AddField(
            model_name='theme',
            name='slogan',
            field=models.CharField(max_length=50, null=True),
            preserve_default=True,
        ),
    ]
