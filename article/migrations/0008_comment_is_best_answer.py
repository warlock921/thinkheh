# -*- coding: utf-8 -*-
# Generated by Django 1.11.8 on 2017-12-25 15:48
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('article', '0007_comment'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='is_best_answer',
            field=models.BooleanField(default=False),
        ),
    ]
