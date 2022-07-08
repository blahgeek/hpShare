#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import getpass
import argparse
import hashlib
import logging
from pathlib import Path

import requests
import qiniu


logger = logging.getLogger('hpshare')


def upload_file(src_file: Path, *,
                username: str,
                passwd: str,
                server: str,
                private: bool,
                enable_checksum: bool):
    logging.info(f'Uploading {src_file}')

    sha1sum = ''
    if enable_checksum:
        h = hashlib.sha1()
        with src_file.open('rb') as f:
            while (buf := f.read(4096)):
                h.update(buf)
            sha1sum = h.hexdigest()

    permit_resp = requests.post(f'https://{server}/~api/hpshare/permit/',
                                auth=(username, passwd),
                                data = {
                                    'filename': src_file.name,
                                    'sha1sum': sha1sum,
                                    'private': 'true' if private else '',
                                    'fsize': src_file.stat().st_size,
                                }).json()
    logger.debug(f'Permit result: {permit_resp}')

    token = permit_resp['token']
    assert token

    put_resp, put_info = qiniu.put_file(token, key=None, file_path=str(src_file.resolve()),
                                        part_size=32 * 1024 * 1024)
    logger.debug(f'Upload done: {put_resp}, {put_info}')
    logger.info(f'Upload done: {put_resp["url"]}')


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('file', nargs='+')
    parser.add_argument('-u', '--user', default=getpass.getuser())
    parser.add_argument('-p', '--private', action='store_true')
    parser.add_argument('-s', '--server', default='share.z1k.dev')
    parser.add_argument('-d', '--debug', action='store_true')
    parser.add_argument('-c', '--checksum', action='store_true')
    args = parser.parse_args()

    logger.setLevel(level=logging.DEBUG if args.debug else logging.INFO)
    logging.basicConfig(level=logging.DEBUG if args.debug else logging.INFO)

    passwd = getpass.getpass()

    for src_file in args.file:
        upload_file(Path(src_file),
                    username=args.user, passwd=passwd,
                    server=args.server, private=args.private,
                    enable_checksum=args.checksum)
