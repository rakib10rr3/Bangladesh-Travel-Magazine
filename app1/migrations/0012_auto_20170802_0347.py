# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-08-01 21:47
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app1', '0011_auto_20170802_0319'),
    ]

    operations = [
        migrations.AlterField(
            model_name='place',
            name='name',
            field=models.TextField(max_length=50),
        ),
    ]
