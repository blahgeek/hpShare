# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2016-01-23 16:47
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='HashID',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('private', models.BooleanField(default=False)),
                ('create_time', models.DateTimeField(auto_now_add=True)),
                ('last_access_time', models.DateTimeField(auto_now=True)),
                ('view_count', models.IntegerField(default=0)),
            ],
        ),
    ]