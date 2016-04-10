#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Created by i@BlahGeek.com at 2016-04-10

import os
from . import SubprocessBaseFop


class PDF2HTMLex(SubprocessBaseFop):
    name = 'pdf2htmlex'

    def _get_io_filename(self, cmd, options):
        return 'content.pdf', 'content.html'

    def _get_cmd(self, cmd, options, input_filename, output_filename):
        height = 800
        if cmd:
            height = int(cmd)
        return ['pdf2htmlEX',
                '--fit-height', str(height),
                '--data-dir', os.path.join(os.getcwd(), 'data/pdf2htmlex'),
                input_filename]

