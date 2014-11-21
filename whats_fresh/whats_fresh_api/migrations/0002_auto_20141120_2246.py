# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations
from django.contrib.auth.models import Group


def create_group(apps, schema_editor):
    Group.objects.get_or_create(name='Data Entry Users')
    return


class Migration(migrations.Migration):

    dependencies = [
        ('whats_fresh_api', '0001_initial'),
        ('auth', '0001_initial')
    ]

    operations = [
        migrations.RunPython(create_group)
    ]
