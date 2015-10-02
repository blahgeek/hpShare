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

    wm_op = ('watermark/1/image/' +
             urlsafe_b64encode(req.build_absolute_uri(STATIC_URL + 'ribbon.png')) +
             '/gravity/NorthWest/dx/0/dy/0')
    wm_video_op = ('wmImage/' + urlsafe_b64encode(req.build_absolute_uri(STATIC_URL + 'ribbon.png')) + 
                   '/wmGravity/NorthWest')

    # Office document to PDF
    if ext in ("doc", "docx", "odt", "rtf", "wps", 
               "ppt", "pptx", "odp", "dps", 
               "xls", "xlsx", "ods", "csv", "et"):
        ops.append(('yifangyun_preview', '.pdf', 'PDF'))

    # Markdown to HTML
    if ext in ('markdown', 'md', 'mkd'):
        css = req.build_absolute_uri(STATIC_URL + 'markdown.css')
        css = urlsafe_b64encode(css)
        ops.append(('md2html/0/css/' + css, '.html', 'HTML'))

    # Image preview (with watermark)
    if ext in ('bmp', 'cr2', 'crw', 'dot', 'eps', 'gif',
               'ico', 'jpeg', 'jpg', 'png', 'ps', 'psd',
               'psb', 'tga', 'ttf', ):
        op = ('imageView2/2/w/1280' + 
              '/format/jpg' + 
              '/interlace/1/')
        op += '|' + wm_op
        ops.append((op, '.preview.jpg', 'Preview'))

    # Video, generate gif or jpg(one frame) depends on file size
    if ext in ('avi', 'mp4', 'wmv', 'mkv', 'ts', 'webm', 
               'mov', 'flv', 'ogv', ):
        if storage.size > 32 * 1024 * 1024: # 32MB
            op = 'vframe/jpg/offset/3' + '|' + wm_op
            ops.append((op, '.preview.jpg', 'Preview'))
        else:
            op = 'avthumb/gif/an/1/r/5/' + wm_video_op
            ops.append((op, '.preview.gif', 'Preview'))
    return ops
