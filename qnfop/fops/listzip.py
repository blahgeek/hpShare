#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# @Author: BlahGeek
# @Date:   2016-08-09
# @Last Modified by:   BlahGeek
# @Last Modified time: 2016-08-14

import zipfile
import json
import os
from . import FileBaseFop


class ListzipOp(FileBaseFop):
    name = 'listzip'

    def process_file(self, tempdir, input_filename, **kwargs):
        with zipfile.ZipFile(os.path.join(tempdir, input_filename), 'r') as f:
            return json.dumps([{
                'filename': x.filename,
                'date_time': x.date_time,
                'compress_size': x.compress_size,
                'file_size': x.file_size,
            } for x in f.infolist()])
