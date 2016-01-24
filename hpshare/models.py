#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Created by i@BlahGeek.com at 2015-01-29

from django.db import models
from hashid.models import HashID

class Storage(models.Model):
    hashid = models.OneToOneField(HashID, on_delete=models.CASCADE, related_name='hpshare_storage')
    filename = models.CharField(max_length=1024)

    persist = models.BooleanField(default=False)
    uploaded = models.BooleanField(default=False)
    size = models.IntegerField(default=0)  # File size in bytes
    mimetype = models.CharField(max_length=255, default='application/octet-stream')
    extension = models.CharField(max_length=255, default='')
    extrainfo = models.CharField(max_length=255, default='')
    sha1sum = models.CharField(max_length=40, default='')
    persistentId = models.CharField(max_length=255, default='', db_index=True)

    download_count = models.IntegerField(default=0)

    def __unicode__(self):
        return self.key_name

    @property
    def key_name(self):
        return '/'.join([self.hashid.hashid, self.filename])

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

class ConvertedStorage(models.Model):
    hashid = models.OneToOneField(HashID, on_delete=models.CASCADE,
                                  related_name='hpshare_converted_storage')
    source = models.ForeignKey(Storage, db_index=True, 
                               related_name='converted_storage')
    success = models.BooleanField()
    error_msg = models.CharField(max_length=255)

    key = models.CharField(max_length=1024)
    cmd = models.CharField(max_length=255)

    description = models.CharField(max_length=255, default='')
    suffix = models.CharField(max_length=255, default='')

    download_count = models.IntegerField(default=0)

    @property
    def filename(self):
        return self.source.filename + self.suffix
    

class StorageGroup(models.Model):
    hashid = models.OneToOneField(HashID, on_delete=models.CASCADE,
                                  related_name='hpshare_storage_group')
    storages = models.ManyToManyField(Storage, related_name='groups')

    persist = models.BooleanField(default=False)

    def delete_safe(self):
        self.storages.clear()
        self.delete()
