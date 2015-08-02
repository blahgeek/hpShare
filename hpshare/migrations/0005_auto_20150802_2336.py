# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('hpshare', '0004_auto_20150802_1952'),
    ]

    operations = [
        migrations.AddField(
            model_name='convertedstorage',
            name='description',
            field=models.CharField(default=b'', max_length=255),
        ),
        migrations.AddField(
            model_name='convertedstorage',
            name='suffix',
            field=models.CharField(default=b'', max_length=255),
        ),
        migrations.AlterField(
            model_name='convertedstorage',
            name='id',
            field=models.UUIDField(default=uuid.uuid4, serialize=False, primary_key=True),
        ),
    ]
