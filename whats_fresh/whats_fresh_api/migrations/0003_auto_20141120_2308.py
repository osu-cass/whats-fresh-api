# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('whats_fresh_api', '0002_auto_20141120_2246'),
    ]

    operations = [
        migrations.AlterField(
            model_name='image',
            name='name',
            field=models.TextField(default=b''),
        ),
        migrations.AlterField(
            model_name='video',
            name='name',
            field=models.TextField(default=b''),
        ),
    ]
