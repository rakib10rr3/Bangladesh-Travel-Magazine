# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-08-01 21:19
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app1', '0010_auto_20170802_0314'),
    ]

    operations = [
        migrations.AlterField(
            model_name='story',
            name='story_page',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='app1.Place'),
        ),
    ]