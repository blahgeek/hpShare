# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('hpshare', '0007_remove_storage_preview_count'),
    ]

    operations = [
        migrations.CreateModel(
            name='StorageGroup',
            fields=[
                ('id', models.CharField(max_length=255, serialize=False, primary_key=True)),
                ('create_time', models.DateTimeField(auto_now_add=True)),
                ('persist', models.BooleanField(default=False)),
                ('view_count', models.IntegerField(default=0)),
                ('storages', models.ManyToManyField(related_name='groups', to='hpshare.Storage')),
            ],
        ),
    ]
