# -*- coding: utf-8 -*-
# Generated by Django 1.11.8 on 2018-01-18 15:36
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('imageload', '0002_auto_20180116_1434'),
    ]

    operations = [
        migrations.AlterField(
            model_name='imageload',
            name='image',
            field=models.ImageField(blank=True, upload_to='images/%Y/%m/%d'),
        ),
    ]
