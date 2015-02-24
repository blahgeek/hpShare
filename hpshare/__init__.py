#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Created by i@BlahGeek.com at 2015-01-29

from __future__ import absolute_import

import config
import qiniu

qn = qiniu.Auth(config.ACCESS_KEY, config.SECRET_KEY)
qn_bucket_mng = qiniu.BucketManager(qn)
