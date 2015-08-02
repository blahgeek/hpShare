# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('hpshare', '0002_storage_preview_count'),
    ]

    operations = [
        migrations.AddField(
            model_name='storage',
            name='persistentId',
            field=models.CharField(default=b'', max_length=255),
        ),
    ]
