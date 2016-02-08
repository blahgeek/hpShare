#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Created by i@BlahGeek.com at 2016-02-08

import functools
import base64
from django.http import HttpResponse
from django.contrib.auth import authenticate

class HttpResponseUnauthorized(HttpResponse):
    status_code = 401
    def __init__(self, realm):
        super(HttpResponseUnauthorized, self).__init__('Basic auth required')
        self['WWW-Authenticate'] = 'Basic realm="{}"'.format(realm)

def http_basic_auth(func):
    @functools.wraps(func)
    def wrap(req, *args, **kwargs):
        meth, auth = req.META.get('HTTP_AUTHORIZATION', '= =').split(' ', 1)
        if meth.lower() == 'basic':
            auth = auth.strip().decode('base64')
            username, password = auth.split(':', 1)
            user = authenticate(username=username, password=password)
            if user:
                req.user = user
        if not req.user.is_authenticated():
            return HttpResponseUnauthorized("User login")
        return func(req, *args, **kwargs)
    return wrap
