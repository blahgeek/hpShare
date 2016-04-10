#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Created by i@BlahGeek.com at 2016-03-20

import tempfile
import os
import subprocess
import shutil
import logging

class BaseFop(object):
    name = None
    require_content = False
    def process(self, cmd, options, content=None):
        raise NotImplemented()


class SubprocessBaseFop(BaseFop):
    require_content = True

    def _get_io_filename(self, cmd, options):
        return 'input.dat', 'output.dat'

    def _get_cmd(self, cmd, options, input_filename, output_filename):
        return ['cp', input_filename, output_filename]

    def process(self, cmd, options, content):
        tempdir = tempfile.mkdtemp()
        input_filename, output_filename = self._get_io_filename(cmd, options)

        input_path = os.path.join(tempdir, input_filename)
        output_path = os.path.join(tempdir, output_filename)

        with open(input_path, 'wb') as input_f:
            input_f.write(content)
        cmd = self._get_cmd(cmd, options, input_filename, output_filename)
        logging.info("Running cmd: {} in {}".format(cmd, tempdir))
        subprocess.check_call(cmd, cwd=tempdir)
        with open(output_path, 'rb') as output_f:
            ret = output_f.read()

        shutil.rmtree(tempdir)
        return ret


__all__ = ['highlight', 'pdf2htmlex', ]
