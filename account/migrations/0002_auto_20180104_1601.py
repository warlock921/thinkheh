# -*- coding: utf-8 -*-
# Generated by Django 1.11.8 on 2018-01-04 16:01
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='last_article_id',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='user_ip',
            field=models.CharField(blank=True, max_length=18, null=True),
        ),
    ]
