# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import hpshare.models


class Migration(migrations.Migration):

    dependencies = [
        ('hpshare', '0005_auto_20150802_2336'),
    ]

    operations = [
        migrations.AlterField(
            model_name='convertedstorage',
            name='id',
            field=models.CharField(default=hpshare.models._uuid, max_length=64, serialize=False, primary_key=True),
        ),
    ]
