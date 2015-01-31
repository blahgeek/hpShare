#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Created by i@BlahGeek.com at 2015-01-31

import requests
import getpass
import sys

URL = 'http://f.blaa.ml/'
UPLOAD_URL = 'http://up.qiniu.com'

if len(sys.argv) < 2:
    print 'Usage:', sys.argv[0], 'FILE'
    sys.exit(0)

filename = sys.argv[1]

username = raw_input('Username: ').strip()
password = getpass.getpass('Password: ').strip()

print >> sys.stderr, 'Preparing to upload...'
req = requests.post(URL + 'permit/', data={'filename': filename}, 
                    auth=(username, password))
req.raise_for_status()
ret = req.json()

print >> sys.stderr, 'Uploading to', ret['key']
req = requests.post(UPLOAD_URL, data=ret, files={
                        'file': open(filename, 'rb')
                    })
req.raise_for_status()
ret = req.json()

print >> sys.stderr, 'Upload done. ID =', ret['id']
print 'URL:', ret['url']

