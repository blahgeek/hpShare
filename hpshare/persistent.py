#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Created by i@BlahGeek.com at 2015-08-02

from base64 import urlsafe_b64encode
from hpurl.settings import STATIC_URL
import config

def get_persistents(req, storage):
    ''' return list of: [OP, Filename_suffix, Description, is_preview] '''
    ops = list()
    ext = '' if ('.' not in storage.filename) else storage.filename.split('.')[-1]
    ext = ext.lower()

    # Office document to PDF
    if ext in ("doc", "docx", "odt", "rtf", "wps",
               "ppt", "pptx", "odp", "dps",
               "xls", "xlsx", "ods", "csv", "et"):
        ops.append(('yifangyun_preview', '.pdf', 'PDF', False))

    # Markdown to HTML
    if ext in ('markdown', 'md', 'mkd'):
        css = req.build_absolute_uri(STATIC_URL + 'markdown.css')
        css = urlsafe_b64encode(css)
        ops.append(('md2html/0/css/' + css, '.html', 'HTML', False))

    # Image preview (original format) (with watermark)
    if ext in ('gif', 'jped', 'jpg', 'png'):
        op = 'imageView2/2/w/1280'
        ops.append((op, '.preview.' + ext.encode('utf8'), 'image', True))
    # Image preview (convert to jpg) (with watermark)
    if ext in ('bmp', 'cr2', 'crw', 'dot', 'eps',
               'ico', 'ps', 'psd', 'psb', 'tga', 'ttf',):
        op = ('imageView2/2/w/1280' +
              '/format/jpg' +
              '/interlace/1/')
        ops.append((op, '.preview.jpg', 'image', True))

    if ext in ('avi', 'mp4', 'wmv', 'mkv', 'ts', 'webm',
               'mov', 'flv', 'ogv', 'm4v', "rm", "m2v"):
        ops.append(('avthumb/mp4/vcodec/libx264/vb/2m/r/30/s/1280x720/autoscale/1/stripmeta/1/',
                    '.preview.mp4', 'video-full', True))
        ops.append(('vframe/jpg/offset/3|imageView2/2/w/1280/h/720/format/jpg',
                    '.poster.jpg', '.video-full-poster', False))

    # try highlight if file size is less than 2M
    if storage.size < 2 * 1024 * 1024 and config.CUSTOM_FOP_NAME:
        ops.append((config.CUSTOM_FOP_NAME + '/highlight',
                    '.highlight.html', 'highlight', True))

    if ext == 'zip' and config.CUSTOM_FOP_NAME:
        ops.append((config.CUSTOM_FOP_NAME + '/listzip', '.listzip.json', 'listzip', True))

    return ops


def get_preview_template(preview_model, model):
    desc = preview_model.description if preview_model is not None else ''

    if desc.startswith('image'):
        return 'preview/image.html'
    if desc == 'video-full':
        return 'preview/video-full.html'
    if desc == 'video/mp4':
        return 'preview/video.html'
    if desc == 'highlight':
        return 'preview/highlight.html'
    # if desc == 'pdf2htmlex':
    #     return 'preview/pdf2htmlex.html'
    if desc == 'listzip':
        return 'preview/listzip.html'

    if model.filename.endswith('asciinema'):
        return 'preview/asciinema.html'

    return None
