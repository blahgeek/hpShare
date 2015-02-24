#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Created by i@BlahGeek.com at 2015-01-29

from __future__ import absolute_import

from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.shortcuts import get_object_or_404, render
from .models import Storage
import urllib
import logging
import config
from . import qn

logger = logging.getLogger(__name__)

def viewfile(req, id):
    try:
        model = Storage.objects.get(id=id)
    except Storage.DoesNotExist:
        return render(req, 'notfound.html')
    model.view_count += 1
    model.save()
    def pretty_size(n):
        if n < 1024:
            return '%d B' % n
        elif n / 1024 < 1024:
            return '%.2f KB' % (n / 1024.0)
        elif n / 1024 / 1024 < 1024:
            return '%.2f MB' % (n / 1024.0 / 1024.0)
        return '%.2f GB' % (n / 1024.0 / 1024.0 / 1024.0)
    return render(req, 'viewfile.html', {
                    'download_url': reverse('downloadfile', args=[id, model.filename]),
                    'preview_url': reverse('previewfile', args=[id, model.filename]),
                    'model': model,
                    'shortmime': model.mimetype.split('/')[0],
                    'pretty_size': pretty_size(model.size),
                  })


def downloadfile(req, id, filename):
    return download_preview_file(req, id, filename, True)

def previewfile(req, id, filename):
    return download_preview_file(req, id, filename, False)

def download_preview_file(req, id, filename, download=True):
    model = get_object_or_404(Storage, id=id)
    if download and req.method == 'GET':  # Do not count 'HEAD'
        model.download_count += 1
        model.save()

    url = config.DOWNLOAD_URL + urllib.quote(model.get_key().encode('utf8'))
    if download:
        url += '?download/'
    return HttpResponseRedirect(qn.private_download_url(url, expires=3600))

