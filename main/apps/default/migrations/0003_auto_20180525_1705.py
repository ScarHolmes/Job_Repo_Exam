# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2018-05-25 17:05
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('default', '0002_job'),
    ]

    operations = [
        migrations.RenameField(
            model_name='job',
            old_name='title',
            new_name='job',
        ),
    ]
