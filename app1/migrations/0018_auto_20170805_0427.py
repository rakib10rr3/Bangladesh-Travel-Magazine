# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-08-04 22:27
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app1', '0017_merge_20170804_2353'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='country',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='app1.Division'),
        ),
    ]