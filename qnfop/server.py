#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Created by i@BlahGeek.com at 2016-03-19

import web
import json
import logging
import requests

from fops import BaseFop
from fops import *
        
urls = (
    '/uop', 'Uop'
)

app = web.application(urls, globals())


_fop_instances = dict()

def find_fop(action):
    def _find(_classes):
        for cls in _classes:
            if cls.name == action:
                if action not in _fop_instances:
                    _fop_instances[action] = cls()
                return _fop_instances[action]
            res = _find(cls.__subclasses__())
            if res:
                return res
        return None
    return _find([BaseFop, ])


class Uop:
    def POST(self):
        data = json.loads(web.data())
        cmd = data['cmd'].split('/')[1:]  # hpurl/cmd/args
        fop = find_fop(cmd[0])
        logging.info('CMD: {}, handler: {}'.format('/'.join(cmd), fop))

        if fop is None:
            return web.notfound()

        content = None
        if fop.require_content:
            content = requests.get(data['src']['url']).content

        return fop.process('/'.join(cmd[1:]), data['src'], content)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    app.run()
