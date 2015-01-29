#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Created by i@BlahGeek.com at 2015-01-29

from django.db import models

class UploadedFile(models.Model):
    file = models.FileField()
    date = models.DateTimeField(auto_now=True)
