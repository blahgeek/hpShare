# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('hashid', '0002_hashid_enabled'),
    ]

    operations = [
        migrations.CreateModel(
            name='Redirection',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('url', models.CharField(max_length=4096)),
                ('permanent', models.BooleanField(default=False)),
                ('hashid', models.OneToOneField(related_name='hpshorten_redirect', on_delete=django.db.models.deletion.PROTECT, to='hashid.HashID')),
            ],
        ),
        migrations.CreateModel(
            name='StaticRedirection',
            fields=[
                ('id', models.CharField(max_length=255, serialize=False, primary_key=True)),
                ('redirection', models.ForeignKey(to='hpshorten.Redirection', on_delete=django.db.models.deletion.PROTECT)),
            ],
        ),
    ]
