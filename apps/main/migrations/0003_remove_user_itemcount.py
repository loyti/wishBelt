# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-07-24 21:46
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0002_auto_20170724_1928'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='itemCount',
        ),
    ]
