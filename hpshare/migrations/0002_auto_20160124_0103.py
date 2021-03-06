# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2016-01-23 17:03
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('hpshare', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='convertedstorage',
            name='hashid',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='hpshare_converted_storage', to='hashid.HashID'),
        ),
        migrations.AlterField(
            model_name='storage',
            name='hashid',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='hpshare_storage', to='hashid.HashID'),
        ),
        migrations.AlterField(
            model_name='storagegroup',
            name='hashid',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='hpshare_storage_group', to='hashid.HashID'),
        ),
    ]
