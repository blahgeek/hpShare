# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2016-02-08 08:07
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hpshorten', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='redirection',
            name='cloak',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='redirection',
            name='title',
            field=models.CharField(default='', max_length=255),
        ),
    ]