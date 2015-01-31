#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Created by i@BlahGeek.com at 2015-01-31

from django.core.management.base import BaseCommand
from hpshare.models import Storage
from hpshare.views import qn_bucket_mng
import qiniu
from datetime import datetime
from django.utils.timezone import utc
from config import STORAGE_EXPIRE, BUCKET_NAME

class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        models = Storage.objects.filter(permit_time__lt=datetime.now()-STORAGE_EXPIRE,
                                        persist=False).all()
        to_delete = list()
        for model in models:
            print 'Deleting', model.get_key(), 
            print (datetime.utcnow().replace(tzinfo=utc) - model.permit_time).days, 'days old'
            to_delete.append(model.get_key())
        if not to_delete:
            print 'Nothing to delete'
            return
        ops = qiniu.build_batch_delete(BUCKET_NAME, to_delete)
        ret, info = qn_bucket_mng.batch(ops)
        models.delete()
        print info

