#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Created by i@BlahGeek.com at 2015-02-24

import config
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
