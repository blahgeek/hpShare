#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Created by i@BlahGeek.com at 2016-03-20

import pygments
import pygments.formatters
import pygments.lexers
from . import BaseFop


class HightLightOP(BaseFop):
    name = 'highlight'
    require_content = True

    def __init__(self):
        self.formatter = pygments.formatters.get_formatter_by_name('html', linenos='table')

    def process(self, cmd, options, content):
        try:
            l = pygments.lexers.get_lexer_for_filename(options.get('key', ''))
        except pygments.lexers.ClassNotFound:
            l = pygments.lexers.guess_lexer(content)
        return pygments.highlight(content, l, self.formatter)
