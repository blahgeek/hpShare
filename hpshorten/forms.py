#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Created by i@BlahGeek.com at 2016-02-08

from django.forms import Form
from django import forms

class ShortenForm(Form):
    private = forms.BooleanField(required=False)
    url = forms.CharField()
    permanent = forms.BooleanField(required=False)
    cloak = forms.BooleanField(required=False)
    title = forms.CharField(required=False)
    static_id = forms.CharField(required=False)
