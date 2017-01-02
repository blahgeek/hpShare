#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Created by i@BlahGeek.com at 2016-02-08

from django.http import HttpResponseBadRequest, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.core.urlresolvers import reverse
from hpurl.auth import http_basic_auth
from .forms import ShortenForm
from hashid.models import HashID
from .models import Redirection, StaticRedirection


@require_POST
@csrf_exempt
@http_basic_auth
def create(req):
    form = ShortenForm(req.POST)
    if not form.is_valid():
        return HttpResponseBadRequest()
    model = Redirection()
    model.hashid = HashID.new(private=form.cleaned_data['private'])
    for key in ('url', 'permanent', 'cloak', 'title'):
        setattr(model, key, form.cleaned_data[key])
    model.save()

    return JsonResponse({
        "url": req.build_absolute_uri(reverse('hpshorten_redirect', args=[model.hashid.hashid, ])),
        "target": model.url
    })


@require_POST
@csrf_exempt
@http_basic_auth
def modify(req, id):
    form = ShortenForm(req.POST)
    if not form.is_valid():
        return HttpResponseBadRequest()
    model = HashID.get_related(id, 'hpshorten_redirect', inc=False)
    for key in ('url', 'permanent', 'cloak', 'title'):
        setattr(model, key, form.cleaned_data[key])
    model.save()

    return JsonResponse({
        "url": req.build_absolute_uri(reverse('hpshorten_redirect', args=[model.hashid.hashid, ])),
        "target": model.url
    })


from django.conf.urls import url

urlpatterns = [
    url(r'^create/', create, name='create'),
    url(r'^modify/R(?P<id>[0-9a-zA-Z]+)/?$', modify, name='modify'),
]
