#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Created by i@BlahGeek.com at 2016-03-20

import tempfile
import os
import subprocess
import shutil
import logging
import requests

class BaseFop(object):
    name = None
    require_content = False
    def process(self, **kwargs):
        '''
        kwargs:

            url: "http://<host>:<port>/<path>",
            mimetype: "<mimetype>",
            fsize: <filesize>,
            bucket: <bucket>,
            key: <key>
            content: ...
            ...
        '''
        raise NotImplemented()


class FileBaseFop(BaseFop):
    require_content = False  # stream the content on my own

    def _get_input_filename(self, **kwargs):
        return 'input.dat'

    def process_file(self, tempdir, input_filename, **kwargs):
        return ''

    def process(self, url, **kwargs):
        tempdir = tempfile.mkdtemp()
        input_filename = self._get_input_filename(**kwargs)

        req = requests.get(url, stream=True)
        with open(os.path.join(tempdir, input_filename), 'wb') as input_f:
            for chunk in req.iter_content(8192):
                input_f.write(chunk)

        try:
            ret = self.process_file(tempdir, input_filename, **kwargs)
        finally:
            shutil.rmtree(tempdir)
        return ret


class SubprocessBaseFop(FileBaseFop):

    def _get_output_filename(self, **kwargs):
        return 'output.dat'

    def _get_cmd(self, input_filename, output_filename, **kwargs):
        return ['cp', input_filename, output_filename]

    def process_file(self, tempdir, input_filename, **kwargs):
        output_filename = self._get_output_filename(**kwargs)
        cmd = self._get_cmd(input_filename, output_filename, **kwargs)

        logging.info("Running cmd: {} in {}".format(cmd, tempdir))
        subprocess.check_call(cmd, cwd=tempdir)
        with open(os.path.join(tempdir, output_filename), 'rb') as output_f:
            ret = output_f.read()
        return ret


__all__ = ['highlight', 'pdf2htmlex', 'listzip']
