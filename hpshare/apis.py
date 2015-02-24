#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Created by i@BlahGeek.com at 2015-02-24

import config
from shortuuid import ShortUUID
from django.core.urlresolvers import reverse
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponseBadRequest, JsonResponse
from django.views.decorators.http import require_POST
from django.shortcuts import get_object_or_404
from .models import Storage
from .forms import PermitForm, CallbackForm
from .auth import qn_callback_auth, http_basic_auth
from . import qn, qn_bucket_mng

@require_POST
@csrf_exempt
@http_basic_auth
def permit(req):
    form = PermitForm(req.POST)
    if not form.is_valid():
        return HttpResponseBadRequest()
    model = Storage()
    model.filename = form.cleaned_data['filename']
    model.user = req.user
    model.id = ShortUUID().random(config.KEY_LENGTH_PRIVATE 
                                  if form.cleaned_data['private'] 
                                  else config.KEY_LENGTH_PUBLIC)
    model.save()

    token = qn.upload_token(config.BUCKET_NAME, model.get_key().encode('utf8'), model.UPLOAD_TIME_LIMIT, {
                                'callbackUrl': req.build_absolute_uri(reverse('callback')),
                                'callbackBody': "extension=$(ext)&mimetype=$(mimeType)&size=$(fsize)&key=$(key)",
                            })
    return JsonResponse({'token': token, 'key': model.get_key()})

@require_POST
@csrf_exempt
@qn_callback_auth
def callback(req):
    form = CallbackForm(req.POST)
    if not form.is_valid():
        return HttpResponseBadRequest()
    id, filename = form.cleaned_data['key'].split('/')
    
    model = get_object_or_404(Storage, id=id)
    model.uploaded = True
    for key in ('size', 'mimetype', 'extension'):
        setattr(model, key, form.cleaned_data[key])
    model.save()

    return JsonResponse({
                            'url': req.build_absolute_uri(reverse('viewfile', args=[id, ])),
                            'id': id,
                        })

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
