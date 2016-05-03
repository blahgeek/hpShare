#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Created by i@BlahGeek.com at 2016-04-10

import os
from . import SubprocessBaseFop


class PDF2HTMLex(SubprocessBaseFop):
    name = 'pdf2htmlex'

    def _get_io_filename(self, **kwargs):
        return 'content.pdf', 'content.html'

    def _get_cmd(self, input_filename, output_filename, 
                 height='800', start_page='1', end_page='5', vdpi='72',
                 **kwargs):
        return ['pdf2htmlEX',
                '--vdpi', vdpi,
                '-f', start_page,
                '-l', end_page,
                '--fit-height', str(height),
                '--data-dir', os.path.join(os.getcwd(), 'data/pdf2htmlex'),
                input_filename]

