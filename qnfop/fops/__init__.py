#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Created by i@BlahGeek.com at 2016-03-20


class BaseFop(object):
    name = None
    require_content = False
    def process(self, cmd, options, content=None):
        raise NotImplemented()

__all__ = ['highlight', ]
