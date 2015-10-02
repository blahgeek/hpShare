#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Created by i@BlahGeek.com at 2015-01-29

from __future__ import absolute_import

from django.http import HttpResponseRedirect, Http404
from django.shortcuts import get_object_or_404, render, redirect
from django.db.models import F
from django.core.exceptions import ObjectDoesNotExist
from django.core.urlresolvers import reverse
from .models import Storage, ConvertedStorage, StorageGroup
from .auth import http_basic_auth
from .persistent import get_preview_html
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

@http_basic_auth
def viewlastfile(req, last_n):
    q = Storage.objects.filter(user=req.user, uploaded=True) \
                        .order_by('-permit_time')
    try:
        q = q[int(last_n)]
    except IndexError:
        raise Http404('Last %d file not found' % int(last_n))
    return redirect('viewfile', q.id)

def viewfile(req, id, disable_preview=False):
    model = get_object_or_404(Storage, id=id)
    model.view_count = F('view_count') + 1
    model.save()

    preview = None
    if not disable_preview:
        preview_model = model.converted_storage\
            .filter(success=True, description__startswith='Preview:')[0:1]
        try:
            preview_model = preview_model.get()
        except ObjectDoesNotExist:
            pass
        else:
            preview_url = reverse('downloadfile_persistent', 
                                  args=(preview_model.id, preview_model.filename))
            preview = get_preview_html(preview_model.description, preview_url)

    return render(req, 'viewfile.html', {
                    'model': model,
                    'preview': preview,
                    'extrainfo': filter(len, model.extrainfo.split('\n')),
                    "persistents": model.converted_storage
                                   .filter(success=True)
                                   .exclude(description__startswith="Preview:"),
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
