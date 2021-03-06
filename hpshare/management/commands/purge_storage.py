#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Created by i@BlahGeek.com at 2015-01-31

from django.core.management.base import BaseCommand
from hpshare.models import Storage, StorageGroup
from hpshare import qn_bucket_mng
from django.utils import timezone
import qiniu
from config import STORAGE_EXPIRE, BUCKET_NAME

def batch_delete(storages):
    to_delete = [x.key_name.encode('utf8') for x in storages]
    for storage in storages:
        to_delete += [x.key.encode('utf8') for x in storage.converted_storage.all()]
    storages.delete()
    ops = qiniu.build_batch_delete(BUCKET_NAME, to_delete)
    return qn_bucket_mng.batch(ops)


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        time_limit = timezone.now()-STORAGE_EXPIRE
        models = Storage.objects.filter(hashid__last_access_time__lt=time_limit,
                                        hashid__create_time__lt=time_limit,
                                        persist=False).all()
        for model in models:
            key_name = model.key_name.encode('utf8')
            print 'Deleting', key_name, 
            print (timezone.now() - model.hashid.create_time).days, 'days old'
        if len(models) == 0:
            print 'Nothing to delete'
            return
        ret, info = batch_delete(models)
        print info

        groups = StorageGroup.objects.filter(hashid__last_access_time__lt=time_limit,
                                             hashid__create_time__le=time_limit,
                                             persist=False).all()
        for group in groups:
            print 'Removing group', group.hashid
            group.delete_safe()
        if len(groups) == 0:
            print "No group to delete"

