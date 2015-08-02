#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Created by i@BlahGeek.com at 2015-08-02

def get_persistents(storage):
    ''' return list of: [OP, Filename_suffix, Description] '''
    ops = list()
    ext = '' if ('.' not in storage.filename) else storage.filename.split('.')[-1]
    if ext in ("doc", "docx", "odt", "rtf", "wps", 
               "ppt", "pptx", "odp", "dps", 
               "xls", "xlsx", "ods", "csv", "et"):
        ops.append(('yifangyun_preview', '.pdf', 'PDF'))
    if ext in ('markdown', 'md', 'mkd'):
        ops.append(('md2html', '.html', 'HTML'))
    return ops