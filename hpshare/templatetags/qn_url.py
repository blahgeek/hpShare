#!/usr/bin/env python2
# -*- coding: utf-8 -*-
# By i@BlahGeek.com at 05/06/2016

from django import template
import config
from .. import qn
import urllib

register = template.Library()

def gen_qn_url(key, download=False):
    url = config.DOWNLOAD_URL + urllib.quote(key.encode('utf8'))
    if download:
        url += '?download/'
    url = qn.private_download_url(url, expires=config.DOWNLOAD_TIME_LIMIT)
    return url

register.filter('qn_url', gen_qn_url)


