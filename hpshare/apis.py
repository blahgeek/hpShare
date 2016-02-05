#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Created by i@BlahGeek.com at 2015-02-24

import config
import uuid
import json
from django.shortcuts import get_object_or_404
from django.core.urlresolvers import reverse
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponseBadRequest, JsonResponse, HttpResponseServerError
from django.views.decorators.http import require_POST
from django.contrib.gis.geoip import GeoIP
from base64 import urlsafe_b64encode
from hashid.models import HashID
from .models import Storage, ConvertedStorage, StorageGroup
from .forms import PermitForm, CallbackForm, NewgroupForm
from .auth import qn_callback_auth, http_basic_auth
from .persistent import get_persistents
from . import qn

geoip = GeoIP()

@require_POST
@csrf_exempt
@http_basic_auth
def permit(req):
    form = PermitForm(req.POST)
    if not form.is_valid():
        return HttpResponseBadRequest()
    model = Storage()
    model.hashid = HashID.new(private=form.cleaned_data['private'])
    model.filename = form.cleaned_data['filename']
    model.sha1sum = form.cleaned_data['sha1sum'].strip()
    model.size = form.cleaned_data['fsize']
    model.save()

    options = {
        'insertOnly': 1,
        'saveKey': model.key_name,
        'fsizeLimit': model.size,
        'callbackUrl': req.build_absolute_uri(reverse('hpshare_api:callback')),
        'callbackBody': CallbackForm.getCallbackBody(),
    }
    if model.sha1sum:
        options['checksum'] = 'SHA1:{}'.format(model.sha1sum)
    persistents = get_persistents(req, model)
    if persistents:
        saveas = config.BUCKET_NAME + ':' + model.key_name.encode('utf8')
        ops = map(lambda x: '{}|saveas/{}'
                  .format(x[0], urlsafe_b64encode(saveas + x[1])), 
                  persistents)
        options['persistentOps'] = ';'.join(ops)
        options['persistentNotifyUrl'] = req.build_absolute_uri(reverse('hpshare_api:persistent_callback'))
        options['persistentPipeline'] = config.PERSISTENT_PIPELINE
    token = qn.upload_token(config.BUCKET_NAME, None, config.UPLOAD_TIME_LIMIT, 
                            options, False)  # strict_policy: false

    country = geoip.country_code(req.META.get('REMOTE_ADDR', ''))
    if country == 'CN' or country is None:
        upload_domain = 'upload.qiniu.com'
    else:
        upload_domain = 'up.qiniug.com'
    return JsonResponse({'token': token, 'upload_domain': upload_domain})

@require_POST
@csrf_exempt
@http_basic_auth
def newgroup(req):
    form = NewgroupForm(req.POST)
    if not form.is_valid():
        return HttpResponseBadRequest()
    ids = form.cleaned_data['ids'].split(',')
    if not ids:
        return HttpResponseBadRequest()

    model = StorageGroup()
    model.hashid = HashID.new(private=form.cleaned_data['private'])
    model.save()

    for id in ids:
        model.storages.add(HashID.get(id).hpshare_storage)
    return JsonResponse({
                        'url': req.build_absolute_uri(reverse('hpshare_viewgroup', args=[model.hashid.hashid,])),
                        'count': len(ids),
                        })

@require_POST
@csrf_exempt
@qn_callback_auth
def callback(req):
    form = CallbackForm(req.POST)
    if not form.is_valid():
        return HttpResponseBadRequest()
    uid, filename = form.cleaned_data['key'].split('/')

    model = get_object_or_404(Storage, uid=uuid.UUID(uid))
    model.uploaded = True
    for key in ('size', 'mimetype', 'extension', 'persistentId'):
        setattr(model, key, form.cleaned_data[key])
    model.extrainfo = '\n'.join(form.extrainfo())
    model.save()

    return JsonResponse({
        'url': req.build_absolute_uri(reverse('hpshare:viewfile', args=[model.hashid.hashid,])),
        'id': model.hashid.hashid,
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
        model.hashid = HashID.new(private=True)
        model.source = source
        model.success = (item['code'] == 0)
        model.error_msg = item.get('error', '')
        model.key = item.get('key', '')
        model.cmd = item['cmd']
        model.suffix, model.description = find_suffix_desc(item['cmd'])
        model.save()
    return JsonResponse({})


from django.conf.urls import url

# app_name = 'hpshare'
urlpatterns = [
    url(r'^permit/', permit, name='permit'),
    url(r'^newgroup/', newgroup, name='newgroup'),
    url(r'^callback/', callback, name='callback'),
    url(r'^p-callback/', persistent_callback, name='persistent_callback'),
]
