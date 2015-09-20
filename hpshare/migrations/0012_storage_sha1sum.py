# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('hpshare', '0011_auto_20150908_1946'),
    ]

    operations = [
        migrations.AddField(
            model_name='storage',
            name='sha1sum',
            field=models.CharField(default=b'', max_length=40),
        ),
    ]
