# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-11-01 17:05
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('skills', '0002_userskill'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userslugs',
            name='slug',
        ),
        migrations.RemoveField(
            model_name='userslugs',
            name='user',
        ),
        migrations.DeleteModel(
            name='UserSlugs',
        ),
    ]