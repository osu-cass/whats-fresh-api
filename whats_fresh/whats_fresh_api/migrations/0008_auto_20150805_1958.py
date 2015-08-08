# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations  # noqa


class Migration(migrations.Migration):

    dependencies = [
        ('whats_fresh_api', '0007_auto_20150804_1916'),
    ]

    operations = [
        migrations.RenameField(
            model_name='theme',
            old_name='site_name',
            new_name='site_title',
        ),
        migrations.RenameField(
            model_name='theme',
            old_name='site_name_slug',
            new_name='site_title_slug',
        ),
    ]
