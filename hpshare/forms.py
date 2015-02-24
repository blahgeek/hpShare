#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Created by i@BlahGeek.com at 2015-01-30

from django.forms import Form
from django import forms

class PermitForm(Form):
    private = forms.BooleanField(required=False)
    filename = forms.CharField()

    def clean_filename(self):
        return self.cleaned_data['filename'].split('/')[-1]


class CallbackForm(Form):
    key = forms.CharField()
    mimetype = forms.CharField()
    extension = forms.CharField()
    size = forms.IntegerField()
