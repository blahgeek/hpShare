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

    def process(self, key, content, **kwargs):
        l = pygments.lexers.guess_lexer_for_filename(key, content)
        return pygments.highlight(content, l, self.formatter)
