# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-12-04 15:56
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('profile', '0006_remove_userprofile_invited_by'),
    ]

    operations = [
        migrations.AddField(
            model_name='languagespoken',
            name='level',
            field=models.CharField(choices=[(b'elementary', b'Elementary knowledge'), (b'medium', b'Medium knowledge'), (b'professional', b'Professional knowlegde'), (b'native_or_bilingual', b'Native or Bilingual')], default=b'elementary', max_length=64),
        ),
    ]
