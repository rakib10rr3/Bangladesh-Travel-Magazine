# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-08-03 19:02
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('app1', '0014_auto_20170804_0057'),
    ]

    operations = [
        migrations.AddField(
            model_name='click_url_track',
            name='by',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='click_url_track',
            name='page_name',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='app1.Place'),
        ),
    ]
