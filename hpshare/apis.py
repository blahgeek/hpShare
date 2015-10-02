#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Created by i@BlahGeek.com at 2015-02-24

import config
import json
import hashids
from django.core.urlresolvers import reverse
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponseBadRequest, JsonResponse, HttpResponseServerError
from django.views.decorators.http import require_POST
from django.shortcuts import get_object_or_404
from django.contrib.gis.geoip import GeoIP
from base64 import urlsafe_b64encode
from .settings import SECRET_KEY
from .models import Storage, ConvertedStorage, StorageGroup, Counter
from .forms import PermitForm, CallbackForm, NewgroupForm
from .auth import qn_callback_auth, http_basic_auth
from .persistent import get_persistents
from . import qn, qn_bucket_mng

geoip = GeoIP()

public_hash = hashids.Hashids(SECRET_KEY, config.KEY_LENGTH_PUBLIC)
private_hash = hashids.Hashids(SECRET_KEY, config.KEY_LENGTH_PRIVATE)

def gen_hashid(private=False):
    uid = Counter.get_newid()
    return private_hash.encode(uid) if private else public_hash.encode(uid)

@require_POST
@csrf_exempt
@http_basic_auth
def permit(req):
    form = PermitForm(req.POST)
    if not form.is_valid():
        return HttpResponseBadRequest()
    model = Storage()
    model.filename = form.cleaned_data['filename']
    model.sha1sum = form.cleaned_data['sha1sum'].strip()
    model.size = form.cleaned_data['fsize']
    model.user = req.user
    model.id = gen_hashid(form.cleaned_data['private'])
    model.save()

    options = {
        'insertOnly': 1,
        'saveKey': model.key_name,
        'fsizeLimit': model.size,
        'callbackUrl': req.build_absolute_uri(reverse('callback')),
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
        options['persistentNotifyUrl'] = req.build_absolute_uri(reverse('persistent_callback'))
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
    model.id = gen_hashid(form.cleaned_data['private'])
    model.save()

    storages = Storage.objects.filter(id__in=ids).all()
    for storage in storages:
        model.storages.add(storage)
    return JsonResponse({
                        'url': req.build_absolute_uri(reverse('viewgroup', args=[model.id,])),
                        'count': len(storages),
                        })

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
    model.extrainfo = '\n'.join(form.extrainfo())
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
        model.id = gen_hashid(True)
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
