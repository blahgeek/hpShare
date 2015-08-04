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


class NewgroupForm(Form):
    private = forms.BooleanField(required=False)
    ids = forms.CharField()


class CallbackForm(Form):
    key = forms.CharField()
    mimetype = forms.CharField()
    extension = forms.CharField(required=False)
    size = forms.IntegerField()
    persistentId = forms.CharField(required=False)

    def clean_extension(self):
        if self.cleaned_data['extension'][0] == '.':
            return self.cleaned_data['extension'][1:]
