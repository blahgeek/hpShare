# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Storage',
            fields=[
                ('id', models.CharField(max_length=255, serialize=False, primary_key=True)),
                ('filename', models.CharField(max_length=1024)),
                ('permit_time', models.DateTimeField(auto_now_add=True)),
                ('persist', models.BooleanField(default=False)),
                ('uploaded', models.BooleanField(default=False)),
                ('size', models.IntegerField(default=0)),
                ('mimetype', models.CharField(default=b'application/octet-stream', max_length=255)),
                ('extension', models.CharField(default=b'', max_length=255)),
                ('view_count', models.IntegerField(default=0)),
                ('download_count', models.IntegerField(default=0)),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
