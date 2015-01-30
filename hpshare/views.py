#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Created by i@BlahGeek.com at 2015-01-29

from __future__ import absolute_import

from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponseBadRequest, JsonResponse, HttpResponseRedirect
from django.views.decorators.http import require_POST
from django.core.urlresolvers import reverse
from django.shortcuts import get_object_or_404, render
from .models import Storage
from .forms import PermitForm, CallbackForm
import logging
import config
import qiniu

qn = qiniu.Auth(config.ACCESS_KEY, config.SECRET_KEY)

logger = logging.getLogger(__name__)

@require_POST
@csrf_exempt
def permit(req):
    form = PermitForm(req.POST)
    if not form.is_valid():
        return HttpResponseBadRequest()
    model = form.save()
    token = qn.upload_token(config.BUCKET_NAME, model.get_key(), 360, 
                            {
                                'callbackUrl': req.build_absolute_uri(reverse('callback')),
                                'callbackBody': "extension=$(ext)&mimetype=$(mimeType)&size=$(fsize)&key=$(key)",
                            })
    return JsonResponse({'token': token, 'key': model.get_key()})

@require_POST
@csrf_exempt
def callback(req):
    form = CallbackForm(req.POST)
    if not form.is_valid():
        return HttpResponseBadRequest()
    data = form.cleaned_data
    id, filename = data['key'].split('/')
    model = get_object_or_404(Storage, id=id)

    model.uploaded = True
    model.size = data['size']
    model.mimetype = data['mimetype']
    model.extension = data['extension']
    model.save()

    return JsonResponse({'url': req.build_absolute_uri(reverse('viewfile', args=[id, filename]))})

def viewfile(req, id, filename):
    model = get_object_or_404(Storage, id=id)
    model.view_count += 1
    model.save()
    def pretty_size(n):
        if n < 1024:
            return '%dB' % n
        elif n / 1024 < 1024:
            return '%.2fKB' % (n / 1024.0)
        elif n / 1024 / 1024 < 1024:
            return '%.2fMB' % (n / 1024.0 / 1024.0)
        return '%.2fGB' % (n / 1024.0 / 1024.0 / 1024.0)
    return render(req, 'viewfile.html', {
                    'url': req.build_absolute_uri(reverse('downloadfile', args=[id, filename])),
                    'filename': model.filename,
                    'size': pretty_size(model.size),
                    'extension': model.extension,
                  })

def downloadfile(req, id, filename):
    model = get_object_or_404(Storage, id=id)
    model.download_count += 1
    model.save()
    return HttpResponseRedirect(config.DOWNLOAD_URL + model.get_key())
