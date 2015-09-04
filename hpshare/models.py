#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Created by i@BlahGeek.com at 2015-01-29

import shortuuid
from django.core.exceptions import ObjectDoesNotExist
from django.db import models
from django.contrib.auth.models import User

class Storage(models.Model):
    id = models.CharField(max_length=255, primary_key=True)
    user = models.ForeignKey(User)
    filename = models.CharField(max_length=1024)

    permit_time = models.DateTimeField(auto_now_add=True)
    last_access_time = models.DateTimeField(auto_now=True)
    persist = models.BooleanField(default=False)
    uploaded = models.BooleanField(default=False)
    size = models.IntegerField(default=0)  # File size in bytes
    mimetype = models.CharField(max_length=255, default='application/octet-stream')
    extension = models.CharField(max_length=255, default='')
    extrainfo = models.CharField(max_length=255, default='')
    persistentId = models.CharField(max_length=255, default='', db_index=True)

    view_count = models.IntegerField(default=0)
    download_count = models.IntegerField(default=0)

    def __unicode__(self):
        return self.key_name

    @property
    def preview(self):
        ret = None
        try:
            ret = self.converted_storage.get(success=True, 
                                             description="Preview")
        except ObjectDoesNotExist:
            pass
        return ret
    

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

def _uuid():
    return shortuuid.uuid()

class ConvertedStorage(models.Model):
    id = models.CharField(primary_key=True, max_length=64, 
                          default=_uuid)

    source = models.ForeignKey(Storage, db_index=True, 
                               related_name='converted_storage')
    success = models.BooleanField()
    error_msg = models.CharField(max_length=255)

    key = models.CharField(max_length=1024)
    cmd = models.CharField(max_length=255)

    complete_time = models.DateTimeField(auto_now_add=True)
    description = models.CharField(max_length=255, default='')
    suffix = models.CharField(max_length=255, default='')

    download_count = models.IntegerField(default=0)

    @property
    def filename(self):
        return self.source.filename + self.suffix
    

class StorageGroup(models.Model):
    id = models.CharField(max_length=255, primary_key=True)
    storages = models.ManyToManyField(Storage, related_name='groups')

    create_time = models.DateTimeField(auto_now_add=True)
    last_access_time = models.DateTimeField(auto_now=True)
    persist = models.BooleanField(default=False)

    view_count = models.IntegerField(default=0)

    def delete_safe(self):
        self.storages.clear()
        self.delete()
