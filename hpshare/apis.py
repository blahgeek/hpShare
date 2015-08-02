#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Created by i@BlahGeek.com at 2015-02-24

import config
import json
from shortuuid import ShortUUID
from django.core.urlresolvers import reverse
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponseBadRequest, JsonResponse, HttpResponseServerError
from django.views.decorators.http import require_POST
from django.shortcuts import get_object_or_404
from base64 import urlsafe_b64encode
from .models import Storage, ConvertedStorage
from .forms import PermitForm, CallbackForm
from .auth import qn_callback_auth, http_basic_auth
from .persistent import get_persistents
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

    options = {
        'insertOnly': 1,
        'saveKey': model.key_name,
        'callbackUrl': req.build_absolute_uri(reverse('callback')),
        'callbackBody': "extension=$(ext)&mimetype=$(mimeType)" +
                        "&size=$(fsize)&key=$(key)" + 
                        "&persistentId=$(persistentId)",
    }
    persistents = get_persistents(req, model)
    if persistents:
        saveas = config.BUCKET_NAME + ':' + model.key_name.encode('utf8')
        ops = map(lambda x: '{}|saveas/{}'
                  .format(x[0], urlsafe_b64encode(saveas + x[1])), 
                  persistents)
        options['persistentOps'] = ';'.join(ops)
        options['persistentNotifyUrl'] = req.build_absolute_uri(reverse('persistent_callback'))
    token = qn.upload_token(config.BUCKET_NAME, None, config.UPLOAD_TIME_LIMIT, 
                            options)
    return JsonResponse({'token': token})

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
    for key in ('size', 'mimetype', 'extension', 'persistentId'):
        setattr(model, key, form.cleaned_data[key])
    model.save()

    return JsonResponse({
        'url': req.build_absolute_uri(reverse('viewfile', args=[id,])),
        'id': id,
    })

@require_POST
@csrf_exempt
def persistent_callback(req):
    data = json.loads(req.body)
    try:
        source = Storage.objects.get(persistentId=data['id'])
    except Storage.DoesNotExist:
        return HttpResponseServerError("Not found, try later.")
    persistents = get_persistents(req, source)
    def find_suffix_desc(cmd):
        for p in persistents:
            if cmd.startswith(p[0]):
                return p[1], p[2]
        return ('', '')
    for item in data['items']:
        model = ConvertedStorage()
        model.source = source
        model.success = (item['code'] == 0)
        model.error_msg = item.get('error', '')
        model.key = item.get('key', '')
        model.cmd = item['cmd']
        model.suffix, model.description = find_suffix_desc(item['cmd'])
        model.save()
    return JsonResponse({})

@require_POST
@csrf_exempt
@http_basic_auth
def deletefile(req):
    model = get_object_or_404(Storage, id=req.POST.get('id', ''))
    ret, info = qn_bucket_mng.delete(config.BUCKET_NAME, model.key_name.encode('utf8'))
    model.delete()
    return JsonResponse({
                            'success': ret is None,
                        })
