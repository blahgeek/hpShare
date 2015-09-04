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

    avinfo_v_codec = forms.CharField(required=False, label='avinfo.video.codec_name')
    avinfo_v_width = forms.IntegerField(required=False, label='avinfo.video.width')
    avinfo_v_height = forms.IntegerField(required=False, label='avinfo.video.height')
    avinfo_v_pixfmt = forms.CharField(required=False, label='avinfo.video.pix_fmt')
    avinfo_v_fps = forms.CharField(required=False, label='avinfo.video.r_frame_rate')

    avinfo_a_codec = forms.CharField(required=False, label='avinfo.audio.codec_name')
    avinfo_a_rate = forms.CharField(required=False, label='avinfo.audio.sample_rate')

    imginfo_width = forms.IntegerField(required=False, label='imageInfo.width')
    imginfo_height = forms.IntegerField(required=False, label='imageInfo.height')
    imginfo_colormodel = forms.CharField(required=False, label='imageInfo.colorModel')

    def clean_extension(self):
        orig = self.cleaned_data['extension']
        return '' if len(orig) <= 1 else orig[1:]

    def extrainfo(self):
        ret = list()
        v = lambda x: self.cleaned_data[x]
        if v('imginfo_width'):
            ret.append('Image: {}x{} @ {}'.format(v('imginfo_width'), v('imginfo_height'), v('imginfo_colormodel')))
            return ret
        if v('avinfo_a_codec'):
            ret.append('Audio: {} {}Hz'.format(v('avinfo_a_codec'), v('avinfo_a_rate')))
        if v('avinfo_v_codec'):
            ret.append('Video: {}({}) {}x{} @ {}fps'.format(v('avinfo_v_codec'),
                       v('avinfo_v_pixfmt'), v('avinfo_v_width'), v('avinfo_v_height'), v('avinfo_v_fps')))
        return ret

    @classmethod
    def getCallbackBody(cls):
        params = ['{}=$({})'.format(key, field.label) 
                  for (key, field) in cls.declared_fields.iteritems()]
        return '&'.join(params)
