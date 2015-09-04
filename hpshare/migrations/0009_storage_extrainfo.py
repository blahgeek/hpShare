# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('hpshare', '0008_storagegroup'),
    ]

    operations = [
        migrations.AddField(
            model_name='storage',
            name='extrainfo',
            field=models.CharField(default=b'', max_length=255),
        ),
    ]
