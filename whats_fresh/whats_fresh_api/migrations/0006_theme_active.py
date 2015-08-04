# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('whats_fresh_api', '0005_auto_20150804_1739'),
    ]

    operations = [
        migrations.AddField(
            model_name='theme',
            name='active',
            field=models.CharField(default=b'No', max_length=5, choices=[(b'Yes', b'Yes'), (b'No', b'No')]),
            preserve_default=True,
        ),
    ]
