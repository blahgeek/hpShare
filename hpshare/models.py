#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Created by i@BlahGeek.com at 2015-01-29

from django.db import models
from django.contrib.auth.models import User

class Storage(models.Model):
    id = models.CharField(max_length=255, primary_key=True)
    user = models.ForeignKey(User)
    filename = models.CharField(max_length=1024)

    permit_time = models.DateTimeField(auto_now_add=True)
    persist = models.BooleanField(default=False)
    uploaded = models.BooleanField(default=False)
    size = models.IntegerField(default=0)  # File size in bytes
    mimetype = models.CharField(max_length=255, default='application/octet-stream')
    extension = models.CharField(max_length=255, default='')

    view_count = models.IntegerField(default=0)
    preview_count = models.IntegerField(default=0)
    download_count = models.IntegerField(default=0)

    @property
    def key_name(self):
        return '/'.join([self.id, self.filename])

    @property
    def readable_size(self):
        n = self.size
        if n < 1024:
            return '%d B' % n
        elif n / 1024 < 1024:
            return '%.2f KB' % (n / 1024.0)
        elif n / 1024 / 1024 < 1024:
            return '%.2f MB' % (n / 1024.0 / 1024.0)
        return '%.2f GB' % (n / 1024.0 / 1024.0 / 1024.0)
