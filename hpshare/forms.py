#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Created by i@BlahGeek.com at 2015-01-30

from django.forms import Form
from django import forms

class PermitForm(Form):
    private = forms.BooleanField(required=False)
    filename = forms.CharField()
    sha1sum = forms.CharField(required=False)
    fsize = forms.IntegerField()

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

    avinfo_format_name = forms.CharField(required=False, label='avinfo.format.format_long_name')
    avinfo_bitrate = forms.IntegerField(required=False, label='avinfo.format.bit_rate')
    avinfo_duration = forms.FloatField(required=False, label='avinfo.format.duration')

    avinfo_v_codec = forms.CharField(required=False, label='avinfo.video.codec_name')
    avinfo_v_bitrate = forms.IntegerField(required=False, label='avinfo.video.bit_rate')
    avinfo_v_width = forms.IntegerField(required=False, label='avinfo.video.width')
    avinfo_v_height = forms.IntegerField(required=False, label='avinfo.video.height')
    avinfo_v_aspect_ratio = forms.CharField(required=False, label='avinfo.video.display_aspect_ratio')
    avinfo_v_pixfmt = forms.CharField(required=False, label='avinfo.video.pix_fmt')
    avinfo_v_fps = forms.CharField(required=False, label='avinfo.video.r_frame_rate')

    avinfo_a_codec = forms.CharField(required=False, label='avinfo.audio.codec_name')
    avinfo_a_rate = forms.CharField(required=False, label='avinfo.audio.sample_rate')
    avinfo_a_bitrate = forms.IntegerField(required=False, label='avinfo.audio.bit_rate')
    avinfo_a_channels = forms.IntegerField(required=False, label='avinfo.audio.channels')

    imginfo_width = forms.IntegerField(required=False, label='imageInfo.width')
    imginfo_height = forms.IntegerField(required=False, label='imageInfo.height')
    imginfo_colormodel = forms.CharField(required=False, label='imageInfo.colorModel')

    def clean_extension(self):
        orig = self.cleaned_data['extension']
        return '' if len(orig) <= 1 else orig[1:]

    def extrainfo(self):
        ret = list()
        v = lambda x: self.cleaned_data[x]
        def info(s, **kwargs):
            _dict = self.cleaned_data.copy()
            _dict.update(kwargs)
            ret.append(s.format(**_dict))

        if v('imginfo_width'):
            info('Image info: {imginfo_width}x{imginfo_height} @ {imginfo_colormodel}')
            return ret
            
        if v('avinfo_format_name') and v('avinfo_v_codec') and v('avinfo_bitrate'):
            info('{avinfo_format_name}, duration: {avinfo_duration:.2f}s, bitrate: {avinfo_bitrate_kb:.2f}kb/s',
                 avinfo_bitrate_kb=v('avinfo_bitrate')/1024.0)
            info('Video stream: {avinfo_v_codec}({avinfo_v_pixfmt}), ' +
                 '{avinfo_v_width}x{avinfo_v_height} [{avinfo_v_aspect_ratio}] @ {avinfo_v_fps}fps, ' + 
                 '{avinfo_v_bitrate_kb:.2f}kb/s',
                 avinfo_v_bitrate_kb=v('avinfo_v_bitrate')/1024.0)

        return ret

    @classmethod
    def getCallbackBody(cls):
        params = ['{}=$({})'.format(key, field.label) 
                  for (key, field) in cls.declared_fields.iteritems()]
        return '&'.join(params)
