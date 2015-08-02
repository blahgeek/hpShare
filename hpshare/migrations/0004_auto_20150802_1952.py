# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('hpshare', '0003_storage_persistentid'),
    ]

    operations = [
        migrations.CreateModel(
            name='ConvertedStorage',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('success', models.BooleanField()),
                ('error_msg', models.CharField(max_length=255)),
                ('key', models.CharField(max_length=1024)),
                ('cmd', models.CharField(max_length=255)),
                ('complete_time', models.DateTimeField(auto_now_add=True)),
                ('download_count', models.IntegerField(default=0)),
            ],
        ),
        migrations.AlterField(
            model_name='storage',
            name='persistentId',
            field=models.CharField(default=b'', max_length=255, db_index=True),
        ),
        migrations.AddField(
            model_name='convertedstorage',
            name='source',
            field=models.ForeignKey(related_name='converted_storage', to='hpshare.Storage'),
        ),
    ]
