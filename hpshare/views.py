#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Created by i@BlahGeek.com at 2015-01-29

from __future__ import absolute_import

from django.http import HttpResponseRedirect, Http404
from django.shortcuts import get_object_or_404, render
from django.db.model import F
from .models import Storage, ConvertedStorage, StorageGroup
import urllib
import logging
import config
from . import qn

logger = logging.getLogger(__name__)

def viewgroup(req, id):
    model = get_object_or_404(StorageGroup, id=id)
    model.view_count = F('view_count') + 1
    model.save()
    storages = list(model.storages.all())
    if len(storages) == 0:
        raise Http404("Group {} has no storage.".format(id))
    return render(req, 'viewgroup.html', {
                     'storages': storages,
                     'model': model,
                 })

def viewfile(req, id, disable_preview=False):
    model = get_object_or_404(Storage, id=id, uploaded=True)
    model.view_count = F('view_count') + 1
    model.save()

    preview = model.preview if not disable_preview else None
    return render(req, 'viewfile.html', {
                    'model': model,
                    'preview': preview,
                    'extrainfo': filter(len, model.extrainfo.split('\n')),
                    "persistents": model.converted_storage
                                   .filter(success=True)
                                   .exclude(description="Preview"),
                  })

def downloadfile_persistent(req, id, filename):
    model = get_object_or_404(ConvertedStorage, id=id, success=True)
    if req.method == 'GET':
        model.download_count = F('download_count') + 1
        model.save()
    url = config.DOWNLOAD_URL + urllib.quote(model.key.encode('utf8'))
    url = qn.private_download_url(url, expires=config.DOWNLOAD_TIME_LIMIT)
    return HttpResponseRedirect(url)

def downloadfile(req, id, filename=''):
    model = get_object_or_404(Storage, id=id, uploaded=True)
    if req.method == 'GET':
        model.download_count = F('download_count') + 1
        model.save()
    url = config.DOWNLOAD_URL + urllib.quote(model.key_name.encode('utf8'))
    url += '?download/'
    url = qn.private_download_url(url, expires=config.DOWNLOAD_TIME_LIMIT)
    return HttpResponseRedirect(url)
