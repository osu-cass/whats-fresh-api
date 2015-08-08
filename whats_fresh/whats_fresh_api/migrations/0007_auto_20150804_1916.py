# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('whats_fresh_api', '0006_theme_active'),
    ]

    operations = [
        migrations.AlterField(
            model_name='theme',
            name='active',
            field=models.CharField(
                default=b'No', unique=True, max_length=5,
                choices=[(b'Yes', b'Yes'), (b'No', b'No')]
                ),
            preserve_default=True,
        ),
    ]
