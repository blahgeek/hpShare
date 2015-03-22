#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Created by i@BlahGeek.com at 2015-01-31

from django.core.management.base import BaseCommand
from hpshare.models import Storage
from hpshare import qn_bucket_mng
from django.utils import timezone
import qiniu
from config import STORAGE_EXPIRE, BUCKET_NAME

class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        models = Storage.objects.filter(permit_time__lt=timezone.now()-STORAGE_EXPIRE,
                                        persist=False).all()
        to_delete = list()
        for model in models:
            key_name = model.key_name.encode('utf8')
            print 'Deleting', key_name, 
            print (timezone.now() - model.permit_time).days, 'days old'
            to_delete.append(key_name)
        if not to_delete:
            print 'Nothing to delete'
            return
        ops = qiniu.build_batch_delete(BUCKET_NAME, to_delete)
        ret, info = qn_bucket_mng.batch(ops)
        models.delete()
        print info

