# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.contrib.auth.models import Group

def create_group(apps, schema_editor):
    if Group.objects.filter(name='Data Entry Users').exists():
        return
    else:
        group = Group.objects.create(name='Data Entry Users')
        group.save()
        return

class Migration(migrations.Migration):

    dependencies = [
        ('whats_fresh_api', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(create_group)
    ]
