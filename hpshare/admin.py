#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Created by i@BlahGeek.com at 2015-01-31

from django.contrib import admin
from django.core.urlresolvers import reverse
from django.utils.html import format_html
from .models import Storage, ConvertedStorage, StorageGroup
from .management.commands.purge_storage import batch_delete

@admin.register(StorageGroup)
class StorageGroupAdmin(admin.ModelAdmin):
    list_display = ('hashid', 'link', 'persist')

    def link(self, obj):
        url = reverse('hpshare_viewgroup', args=[obj.hashid.hashid, ])
        return format_html('<a href="{0}">link</a>', url)
    link.allow_tags = True

    def get_actions(self, req):
        actions = super(StorageGroupAdmin, self).get_actions(req)
        del actions['delete_selected']
        return actions

    actions = ('delete_safe', )
    def delete_safe(self, req, models):
        for model in models:
            model.delete_safe()

    delete_safe.short_description = 'Remove groups without deleting storage'

@admin.register(ConvertedStorage)
class ConvertedStorageAdmin(admin.ModelAdmin):
    list_display = ('source', 'success', "description", "suffix", "is_preview",
                    'download_count')
    ordering = ('hashid__create_time', )

@admin.register(Storage)
class StorageAdmin(admin.ModelAdmin):
    list_display = ('hashid', 'filename', 'link', 'readable_size', 
                    'uploaded', 'download_count', 'persist')
    actions = ('delete_storage', )
    ordering = ('hashid__create_time', )

    def get_actions(self, req):
        actions = super(StorageAdmin, self).get_actions(req)
        del actions['delete_selected']
        return actions

    def link(self, obj):
        url = reverse('hpshare:viewfile', args=[obj.hashid.hashid, ])
        return format_html('<a href="{0}">link</a>', url)
    link.allow_tags = True

    def readable_size(self, obj):
        return obj.readable_size
    readable_size.admin_order_field = 'size'

    def delete_storage(self, req, models):
        ret, info = batch_delete(models)
        self.message_user(req, info)

    delete_storage.short_description = 'Remove files and delete records'
