#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# @Author: BlahGeek
# @Date:   2016-08-09
# @Last Modified by:   BlahGeek
# @Last Modified time: 2016-08-09

import zipfile
import json
from StringIO import StringIO
from . import BaseFop


class ListzipOp(BaseFop):
    name = 'listzip'
    require_content = True

    def process(self, key, content, **kwargs):
        content_f = StringIO(content)
        with zipfile.ZipFile(content_f, 'r') as f:
            return json.dumps([{
                'filename': x.filename,
                'date_time': x.date_time,
                'compress_size': x.compress_size,
                'file_size': x.file_size,
            } for x in f.infolist()])
