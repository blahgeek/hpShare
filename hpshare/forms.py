#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Created by i@BlahGeek.com at 2015-01-30

from django.forms import ModelForm, Form
from django import forms
from .models import Storage

class PermitForm(ModelForm):
    class Meta:
        model = Storage
        fields = ['filename', ]


class CallbackForm(Form):
    key = forms.CharField()
    mimetype = forms.CharField()
    size = forms.IntegerField()
