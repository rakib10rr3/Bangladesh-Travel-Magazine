# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2017-01-22 09:08
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app1', '0006_auto_20170122_1300'),
    ]

    operations = [
        migrations.AlterField(
            model_name='image',
            name='page',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='pages', to='app1.Page'),
        ),
    ]
