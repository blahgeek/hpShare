#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Created by i@BlahGeek.com at 2015-01-29

from __future__ import absolute_import

from django.http import HttpResponseRedirect, Http404
from django.shortcuts import render
from django.db.models import F
from django.core.exceptions import ObjectDoesNotExist
from .persistent import get_preview_template
from hashid.models import HashID
import urllib
import logging
import config
from . import qn

logger = logging.getLogger(__name__)

def viewgroup(req, id):
    model = HashID.get_related(id, 'hpshare_storage_group')
    storages = list(model.storages.all())
    if len(storages) == 0:
        raise Http404("Group {} has no storage.".format(id))
    return render(req, 'viewgroup.html', {
                     'storages': storages,
                     'model': model,
                  })

def viewfile(req, id, disable_preview=False):
    model = HashID.get_related(id, 'hpshare_storage')

    preview_template = None
    preview_model = None
    if not disable_preview:
        preview_model = model.converted_storage\
            .filter(success=True, is_preview=True)[0:1]
        try:
            preview_model = preview_model.get()
        except ObjectDoesNotExist:
            pass
        else:
            preview_template = get_preview_template(preview_model.description)

    persistents = model.converted_storage.filter(success=True, is_preview=False)
    if preview_template is None:
        persistents = list(persistents) + [preview_model, ]
        preview_model = None

    return render(req, 'viewfile.html', {
                    'model': model,
                    'preview_model': preview_model,
                    'preview_template': preview_template,
                    'extrainfo': filter(len, model.extrainfo.split('\n')),
                    "persistents": persistents,
                  })

def downloadfile_persistent(req, id):
    model = HashID.get_related(id, 'hpshare_converted_storage')
    if not model.success:
        raise Http404("File {} is not ready".format(id))
    if req.method == 'GET':
        model.download_count = F('download_count') + 1
        model.save()
    url = config.DOWNLOAD_URL + urllib.quote(model.key.encode('utf8'))
    url = qn.private_download_url(url, expires=config.DOWNLOAD_TIME_LIMIT)
    return HttpResponseRedirect(url)

def downloadfile(req, id):
    model = HashID.get_related(id, 'hpshare_storage')
    if not model.uploaded:
        raise Http404("File {} is not ready".format(id))
    if req.method == 'GET':
        model.download_count = F('download_count') + 1
        model.save()
    url = config.DOWNLOAD_URL + urllib.quote(model.key_name.encode('utf8'))
    url += '?download/'
    url = qn.private_download_url(url, expires=config.DOWNLOAD_TIME_LIMIT)
    return HttpResponseRedirect(url)


from django.conf.urls import url

# app_name = 'hpshare'
urlpatterns = [
    url(r'^(?P<id>[0-9a-zA-Z]+)/?$', viewfile, name='viewfile'),
    url(r'^(?P<id>[0-9a-zA-Z]+)_/?$', viewfile, {'disable_preview': True}),

    url(r'^(?P<id>[0-9a-zA-Z]+)/download/?$', 
        downloadfile, name='downloadfile'),
    # url(r'^(?P<id>[0-9a-zA-Z]+)/download/(?P<filename>[^/]+)$', 
    #     downloadfile, name='downloadfile'),

    url(r'^(?P<id>[0-9a-zA-Z]+)/download2/?$', 
        downloadfile_persistent, name='downloadfile_persistent'),
    # url(r'^(?P<id>[0-9a-zA-Z]+)/download2/(?P<filename>[^/]+)$', 
    #     downloadfile_persistent, name='downloadfile_persistent'),
]
