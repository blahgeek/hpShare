# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('hpshare', '0006_auto_20150802_2350'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='storage',
            name='preview_count',
        ),
    ]
