#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Created by i@BlahGeek.com at 2015-01-31

import functools
import base64
import hmac
from hashlib import sha1
import config
from hpurl.auth import HttpResponseUnauthorized

def qn_callback_auth(func):
    @functools.wraps(func)
    def wrap(req, *args, **kwargs):
        auth = req.META.get('HTTP_AUTHORIZATION', '')
        _, encoded_data = auth.split(':', 1)
        data = req.path + '\n' + req.body
        verify_data = hmac.new(config.SECRET_KEY, data, sha1).digest()
        if base64.urlsafe_b64encode(verify_data) != encoded_data:
            return HttpResponseUnauthorized("Qiniu callback auth")
        return func(req, *args, **kwargs)
    return wrap
