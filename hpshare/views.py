#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Created by i@BlahGeek.com at 2015-01-29

from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, HttpResponseBadRequest
from django.views.decorators.http import require_POST
from .forms import UploadedFileForm

@require_POST
@csrf_exempt
def upload(req):
    form = UploadedFileForm(req.POST, req.FILES)
    if not form.is_valid():
        return HttpResponseBadRequest()
    form.save()
    return HttpResponse('OK')
