# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-03-18 14:33
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('app1', '0005_auto_20170205_1709'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='like',
            name='page',
        ),
        migrations.RemoveField(
            model_name='like',
            name='user',
        ),
        migrations.AddField(
            model_name='story',
            name='likes',
            field=models.ManyToManyField(related_name='likes', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='page',
            name='name',
            field=models.CharField(max_length=50, unique=True),
        ),
        migrations.AlterField(
            model_name='story',
            name='des',
            field=models.TextField(default='', max_length=5000),
        ),
        migrations.DeleteModel(
            name='like',
        ),
    ]
