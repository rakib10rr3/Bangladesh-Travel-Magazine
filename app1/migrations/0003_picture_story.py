# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2017-01-29 20:14
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app1', '0002_auto_20170130_0139'),
    ]

    operations = [
        migrations.AddField(
            model_name='picture',
            name='story',
            field=models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, related_name='stories', to='app1.Story'),
            preserve_default=False,
        ),
    ]