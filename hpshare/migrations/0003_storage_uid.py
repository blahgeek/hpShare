# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2016-02-05 02:34
from __future__ import unicode_literals

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('hpshare', '0002_auto_20160124_0103'),
    ]

    operations = [
        migrations.AddField(
            model_name='storage',
            name='uid',
            field=models.UUIDField(db_index=True, default=uuid.uuid4, editable=False),
        ),
    ]