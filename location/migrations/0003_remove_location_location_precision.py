# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-12-04 09:52
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('location', '0002_distancecacheentry'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='location',
            name='location_precision',
        ),
    ]