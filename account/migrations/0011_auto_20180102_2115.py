# -*- coding: utf-8 -*-
# Generated by Django 1.11.8 on 2018-01-02 21:15
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0010_auto_20180102_2115'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userinfo',
            name='follow_user',
            field=models.ManyToManyField(blank=True, related_name='follow_user', to=settings.AUTH_USER_MODEL),
        ),
    ]