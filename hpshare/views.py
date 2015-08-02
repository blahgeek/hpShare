#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Created by i@BlahGeek.com at 2015-01-29

from __future__ import absolute_import

from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from .models import Storage, ConvertedStorage
import urllib
import logging
import config
from . import qn

logger = logging.getLogger(__name__)

def viewfile(req, id):
    model = get_object_or_404(Storage, id=id, uploaded=True)
    model.view_count += 1
    model.save()

    shortmime = model.mimetype.split('/')[0]
    enable_preview = (shortmime == "image" or
                      (shortmime == "video" and model.size < 10e6) or
                      (shortmime == "audio" and model.size < 5e6))
    return render(req, 'viewfile.html', {
                    'model': model,
                    'shortmime': shortmime,
                    "enable_preview": enable_preview,
                  })

def downloadfile_persistent(req, id, filename):
    model = get_object_or_404(ConvertedStorage, id=id, success=True)
    if req.method == 'GET':
        model.download_count += 1
        model.save()
    url = config.DOWNLOAD_URL + urllib.quote(model.key.encode('utf8'))
    url += '?download/'
    url = qn.private_download_url(url, expires=config.DOWNLOAD_TIME_LIMIT)
    return HttpResponseRedirect(url)

def downloadfile(req, id, filename):
    return download_preview_file(req, id, filename, True)

def previewfile(req, id, filename):
    return download_preview_file(req, id, filename, False)

def download_preview_file(req, id, filename, download=True):
    model = get_object_or_404(Storage, id=id, uploaded=True)
    if req.method == 'GET':  # Do not count 'HEAD'
        if download:
            model.download_count += 1
        else:
            model.preview_count += 1
        model.save()

    url = config.DOWNLOAD_URL + urllib.quote(model.key_name.encode('utf8'))
    if download:
        url += '?download/'
    return HttpResponseRedirect(qn.private_download_url(url, expires=config.DOWNLOAD_TIME_LIMIT))

