#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Created by i@BlahGeek.com at 2015-01-29

from django.db import models
import uuid
import time

def get_file_path(instance, filename):
    return 'uploads/%s-%s/%s' % (time.strftime('%Y%m%d-%H%M'), 
                                 str(uuid.uuid4()).split('-')[0], 
                                 filename)

class UploadedFile(models.Model):
    file = models.FileField(upload_to=get_file_path)
    date = models.DateTimeField(auto_now=True)
