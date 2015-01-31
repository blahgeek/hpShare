#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Created by i@BlahGeek.com at 2015-01-31

import functools
import base64
import hmac
from hashlib import sha1
import config
from django.http import HttpResponseBadRequest, HttpResponseForbidden
from django.contrib.auth import authenticate, login

def qn_callback_auth(func):
    @functools.wraps(func)
    def wrap(req, *args, **kwargs):
        auth = req.META.get('HTTP_AUTHORIZATION', '')
        _, encoded_data = auth.split(':', 1)
        data = req.path + '\n' + req.body
        verify_data = hmac.new(config.SECRET_KEY, data, sha1).digest()
        if base64.urlsafe_b64encode(verify_data) != encoded_data:
            return HttpResponseBadRequest()
        return func(req, *args, **kwargs)
    return wrap

def http_basic_auth(func):
    @functools.wraps(func)
    def wrap(req, *args, **kwargs):
        meth, auth = req.META.get('HTTP_AUTHORIZATION', '= =').split(' ', 1)
        if meth.lower() == 'basic':
            auth = auth.strip().decode('base64')
            username, password = auth.split(':', 1)
            user = authenticate(username=username, password=password)
            if user:
                login(req, user)
        if not req.user.is_authenticated():
            return HttpResponseForbidden()
        return func(req, *args, **kwargs)
    return wrap
