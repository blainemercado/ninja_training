# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-07-26 17:08
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('trips', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='trip',
            name='joined_by',
        ),
        migrations.AddField(
            model_name='trip',
            name='joined_by',
            field=models.ManyToManyField(null=True, related_name='User2', to='trips.User'),
        ),
    ]