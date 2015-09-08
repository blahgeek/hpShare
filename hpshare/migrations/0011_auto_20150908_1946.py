# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('hpshare', '0010_auto_20150904_1948'),
    ]

    operations = [
        migrations.CreateModel(
            name='Counter',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True)),
            ],
        ),
        migrations.AlterField(
            model_name='convertedstorage',
            name='id',
            field=models.CharField(max_length=64, serialize=False, primary_key=True),
        ),
    ]
