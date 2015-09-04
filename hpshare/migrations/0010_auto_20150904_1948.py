# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('hpshare', '0009_storage_extrainfo'),
    ]

    operations = [
        migrations.AddField(
            model_name='storage',
            name='last_access_time',
            field=models.DateTimeField(default=datetime.datetime(2015, 9, 4, 11, 48, 45, 925607, tzinfo=utc), auto_now=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='storagegroup',
            name='last_access_time',
            field=models.DateTimeField(default=datetime.datetime(2015, 9, 4, 11, 48, 53, 500486, tzinfo=utc), auto_now=True),
            preserve_default=False,
        ),
    ]
