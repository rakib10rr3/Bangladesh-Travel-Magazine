# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-03-22 10:21
from __future__ import unicode_literals

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('app1', '0011_auto_20170322_1000'),
    ]

    operations = [
        migrations.AddField(
            model_name='story',
            name='created_date',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]