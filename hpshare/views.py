#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Created by i@BlahGeek.com at 2015-01-29

from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponseBadRequest, JsonResponse
from django.views.decorators.http import require_POST
from .forms import UploadedFileForm
import logging

logger = logging.getLogger(__name__)

@require_POST
@csrf_exempt
def upload(req):
    form = UploadedFileForm(req.POST, req.FILES)
    if not form.is_valid():
        return HttpResponseBadRequest()
    model = form.save()
    logger.info("File uploaded: %s, size: %d", model.file.name, model.file.size)
    return JsonResponse({
                            'url': model.file.url,
                            'size': model.file.size,
                        })
