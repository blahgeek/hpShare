#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Created by i@BlahGeek.com at 2015-01-29

from .models import UploadedFile
from django.forms import ModelForm

class UploadedFileForm(ModelForm):
    class Meta:
        model = UploadedFile
        fields = ['file']
