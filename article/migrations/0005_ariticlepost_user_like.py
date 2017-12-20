# -*- coding: utf-8 -*-
# Generated by Django 1.11.8 on 2017-12-20 22:40
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('article', '0004_auto_20171219_0847'),
    ]

    operations = [
        migrations.AddField(
            model_name='ariticlepost',
            name='user_like',
            field=models.ManyToManyField(blank=True, related_name='articles_like', to=settings.AUTH_USER_MODEL, verbose_name='点赞数'),
        ),
    ]
