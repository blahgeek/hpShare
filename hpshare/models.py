#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Created by i@BlahGeek.com at 2015-01-29

from django.db import models
from django.contrib.auth.models import User
from shortuuid import ShortUUID

class Storage(models.Model):
    id = models.CharField(max_length=255, primary_key=True,
                          default=lambda: ShortUUID().random(8))
    user = models.ForeignKey(User)
    filename = models.CharField(max_length=1024)
    permit_time = models.DateTimeField(auto_now_add=True)
    uploaded = models.BooleanField(default=False)
    size = models.IntegerField(default=0) # File size in bytes
    mimetype = models.CharField(max_length=255, default='application/octet-stream')
    extension = models.CharField(max_length=255, default='')
    view_count = models.IntegerField(default=0)
    download_count = models.IntegerField(default=0)

    def get_key(self):
        return '/'.join([self.id, self.filename])
