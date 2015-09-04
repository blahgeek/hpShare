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
    key = forms.CharField(label='key')
    mimetype = forms.CharField(label='mimeType')
    extension = forms.CharField(required=False, label='ext')
    size = forms.IntegerField(label='fsize')
    persistentId = forms.CharField(required=False, label='persistentId')

    def clean_extension(self):
        orig = self.cleaned_data['extension']
        return '' if len(orig) <= 1 else orig[1:]

    @classmethod
    def getCallbackBody(cls):
        params = ['{}=$({})'.format(key, field.label) 
                  for (key, field) in cls.declared_fields.iteritems()]
        return '&'.join(params)
