# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('hashid', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='hashid',
            name='enabled',
            field=models.BooleanField(default=True),
        ),
    ]
