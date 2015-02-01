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
import urllib
import logging
import config
import qiniu
from .auth import qn_callback_auth, http_basic_auth

qn = qiniu.Auth(config.ACCESS_KEY, config.SECRET_KEY)
qn_bucket_mng = qiniu.BucketManager(qn)

logger = logging.getLogger(__name__)

@require_POST
@csrf_exempt
@http_basic_auth
def permit(req):
    form = PermitForm(req.POST)
    if not form.is_valid():
        return HttpResponseBadRequest()
    model = form.save(commit=False)
    model.user = req.user
    model.save()

    token = qn.upload_token(config.BUCKET_NAME, model.get_key().encode('utf8'), 360, 
                            {
                                'callbackUrl': req.build_absolute_uri(reverse('callback')),
                                'callbackBody': "extension=$(ext)&mimetype=$(mimeType)&size=$(fsize)&key=$(key)",
                            })
    return JsonResponse({
                            'token': token, 
                            'key': model.get_key(),
                        })

@require_POST
@csrf_exempt
@qn_callback_auth
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

    return JsonResponse({
                            'url': req.build_absolute_uri(reverse('viewfile', args=[id, ])),
                            'id': id,
                        })

def viewfile(req, id):
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
                    'url': reverse('downloadfile', args=[id, model.filename]),
                    'filename': model.filename,
                    'size': pretty_size(model.size),
                    'extension': model.extension,
                    'time': model.permit_time,
                  })

def downloadfile(req, id, filename):
    model = get_object_or_404(Storage, id=id)
    model.download_count += 1
    model.save()

    url = config.DOWNLOAD_URL + urllib.quote(model.get_key().encode('utf8'))
    url += '?download/'
    return HttpResponseRedirect(qn.private_download_url(url, expires=3600))


@require_POST
@csrf_exempt
@http_basic_auth
def deletefile(req):
    model = get_object_or_404(Storage, id=req.POST.get('id', ''))
    ret, info = qn_bucket_mng.delete(config.BUCKET_NAME, model.get_key().encode('utf8'))
    model.delete()
    return JsonResponse({
                            'success': ret is None,
                        })
