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

    wm_op = ('watermark/1/image/' +
             urlsafe_b64encode(req.build_absolute_uri(STATIC_URL + 'ribbon.png')) +
             '/gravity/NorthWest/dx/0/dy/0')
    wm_video_op = ('wmImage/' + urlsafe_b64encode(req.build_absolute_uri(STATIC_URL + 'ribbon.png')) + 
                   '/wmGravity/NorthWest')

    pdf_preview_op = config.CUSTOM_FOP_NAME + '/pdf2htmlex/height/800/start_page/1/end_page/5'

    # Office document to PDF
    if ext in ("doc", "docx", "odt", "rtf", "wps", 
               "ppt", "pptx", "odp", "dps", 
               "xls", "xlsx", "ods", "csv", "et"):
        ops.append(('yifangyun_preview', '.pdf', 'PDF', False))
        ops.append(('yifangyun_preview' + '|' + pdf_preview_op, 
                    '.pdf.html', 'pdf2htmlex', True))

    # Preview PDF
    if ext in ('pdf', ):
        ops.append((pdf_preview_op, '.html', 'pdf2htmlex', True))

    # Markdown to HTML
    if ext in ('markdown', 'md', 'mkd'):
        css = req.build_absolute_uri(STATIC_URL + 'markdown.css')
        css = urlsafe_b64encode(css)
        ops.append(('md2html/0/css/' + css, '.html', 'HTML', False))

    # Image preview (original format) (with watermark)
    if ext in ('gif', 'jped', 'jpg', 'png'):
        op = 'imageView2/2/w/1280' + '|' + wm_op
        ops.append((op, '.preview.' + ext.encode('utf8'), 'image', True))
    # Image preview (convert to jpg) (with watermark)
    if ext in ('bmp', 'cr2', 'crw', 'dot', 'eps',
               'ico', 'ps', 'psd', 'psb', 'tga', 'ttf',):
        op = ('imageView2/2/w/1280' + 
              '/format/jpg' + 
              '/interlace/1/')
        op += '|' + wm_op
        ops.append((op, '.preview.jpg', 'image', True))

    # Video, convert to mp4(h.264) without audio, 30 second at most
    if ext in ('avi', 'mp4', 'wmv', 'mkv', 'ts', 'webm', 
               'mov', 'flv', 'ogv', ):
        op = ('avthumb/mp4/an/1/vcodec/libx264/' + 
              't/30/s/1080x720/autoscale/1/stripmeta/1/' +
              wm_video_op)
        ops.append((op, '.preview.mp4', 'video/mp4', True))

    # try highlight if file size is less than 2M
    if storage.size < 2 * 1024 * 1024:
        ops.append((config.CUSTOM_FOP_NAME + '/highlight', 
                    '.highlight.html', 'highlight', True))

    return ops


def get_preview_template(desc):
    if desc.startswith('image'):
        return 'preview/image.html'
    if desc.startswith('video'):
        return 'preview/video.html'
    if desc == 'highlight':
        return 'preview/highlight.html'
    if desc == 'pdf2htmlex':
        return 'preview/pdf2htmlex.html'
    return None
