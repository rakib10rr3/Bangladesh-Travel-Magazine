# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-07-28 10:03
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('app1', '0005_userprofile_follows'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userprofile',
            name='follows',
        ),
        migrations.AddField(
            model_name='userprofile',
            name='follows',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='follows', to=settings.AUTH_USER_MODEL),
        ),
    ]
