# -*- coding: utf-8 -*-
# Generated by Django 1.11.8 on 2017-12-21 20:18
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0005_auto_20171214_1918'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='user_ip',
            field=models.CharField(max_length=18, null=True),
        ),
    ]