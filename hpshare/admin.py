#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Created by i@BlahGeek.com at 2015-01-31

from django.contrib import admin
from django.core.urlresolvers import reverse
from django.utils.html import format_html
from .models import Storage, ConvertedStorage
from .management.commands.purge_storage import batch_delete

@admin.register(ConvertedStorage)
class ConvertedStorageAdmin(admin.ModelAdmin):
    list_display = ('source', 'success', 'cmd', 'complete_time', 'download_count')
    ordering = ('complete_time', )

@admin.register(Storage)
class StorageAdmin(admin.ModelAdmin):
    list_display = ('key_name', 'link', 'user', 'readable_size', 'permit_time', 
                    'uploaded', 'view_count', 'preview_count', 'download_count', 'persist')
    actions = ('delete_storage', )
    ordering = ('permit_time', )

    def get_actions(self, req):
        actions = super(StorageAdmin, self).get_actions(req)
        del actions['delete_selected']
        return actions

    def link(self, obj):
        url = reverse('viewfile', args=[obj.id, ])
        return format_html('<a href="{0}">link</a>', url)
    link.allow_tags = True

    def readable_size(self, obj):
        return obj.readable_size
    readable_size.admin_order_field = 'size'

    def delete_storage(self, req, models):
        ret, info = batch_delete(models)
        self.message_user(req, info)

    delete_storage.short_description = 'Remove files and delete records'
