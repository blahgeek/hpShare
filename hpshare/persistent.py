#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Created by i@BlahGeek.com at 2015-08-02

from base64 import urlsafe_b64encode
from .settings import STATIC_URL

def get_persistents(req, storage):
    ''' return list of: [OP, Filename_suffix, Description] '''
    ops = list()
    ext = '' if ('.' not in storage.filename) else storage.filename.split('.')[-1]
    ext = ext.lower()

    if ext in ("doc", "docx", "odt", "rtf", "wps", 
               "ppt", "pptx", "odp", "dps", 
               "xls", "xlsx", "ods", "csv", "et"):
        ops.append(('yifangyun_preview', '.pdf', 'PDF'))
    if ext in ('markdown', 'md', 'mkd'):
        css = req.build_absolute_uri(STATIC_URL + 'markdown.css')
        css = urlsafe_b64encode(css)
        ops.append(('md2html/0/css/' + css, '.html', 'HTML'))
    if ext in ('bmp', 'cr2', 'crw', 'dot', 'eps', 'gif',
               'ico', 'jpeg', 'jpg', 'png', 'ps', 'psd',
               'psb', 'tga', 'ttf', ):
        op = ('imageView2/2/w/1280' + 
              '/format/jpg' + 
              '/interlace/1/')
        op += '|' + ('watermark/2/text/' + urlsafe_b64encode('hpShare') + 
                     '/font/' + urlsafe_b64encode('times new roman') +
                     '/fontsize/1000/fill/' + urlsafe_b64encode('white') + 
                     '/dissolve/50/gravity/NorthWest/dx/20/dy/10')
        ops.append((op, '.preview.jpg', 'Preview'))
    return ops
