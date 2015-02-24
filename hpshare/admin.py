#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Created by i@BlahGeek.com at 2015-01-31

from django.contrib import admin
from django.core.urlresolvers import reverse
from django.utils.html import format_html
from .models import Storage
from config import BUCKET_NAME
from . import qn_bucket_mng
import qiniu

@admin.register(Storage)
class StorageAdmin(admin.ModelAdmin):
    list_display = ('key_name', 'link', 'user', 'readable_size', 'permit_time', 
                    'uploaded', 'view_count', 'download_count', 'persist')
    actions = ('delete_storage', )
    ordering = ('permit_time', )

    def link(self, obj):
        url = reverse('viewfile', args=[obj.id, ])
        return format_html('<a href="{0}">link</a>', url)
    link.allow_tags = True

    def readable_size(self, obj):
        return obj.readable_size
    readable_size.admin_order_field = 'size'

    def delete_storage(self, req, models):
        to_delete = [x.key_name.encode('utf8') for x in models]
        ops = qiniu.build_batch_delete(BUCKET_NAME, to_delete)
        qn_bucket_mng.batch(ops)
        models.delete()
        self.message_user(req, '%d files deleted' % len(to_delete))

    delete_storage.short_description = 'Remove files and delete records'
