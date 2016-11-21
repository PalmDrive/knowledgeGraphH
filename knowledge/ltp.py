# coding=utf8
from __future__ import absolute_import

import urllib
import argparse
import json

API_KEY = 'K8L7C0w9yxVGAK3Q7q3euHtsbtfzOgMsya4Fyb8x'

DependencyParsing = {
    'sbv', 'forward',  # 主谓关系
    'vob', 'forward',  # 动宾关系
    'iob', 'forward',  # 间宾关系
    'fob', 'backward'  # 前置宾语
}


class Ltp(object):

    def call(self, text, pattern):
        return urllib.urlopen(self.get_url(text, pattern)).read()

    def get_url(self, text, pattern):
        params = {
            "api_key": API_KEY,
            "text": text,
            "pattern": pattern,
            "format": "json",
        }
        url = 'http://api.ltp-cloud.com/analysis/?' + urllib.urlencode(params)
        return url


def handle_request(response):
    body = json.loads(response)
    return body


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument(
        'text', help='text')
    parser.add_argument(
        'pattern', help='pattern = dp, sdp, srl or all')
    args = parser.parse_args()
    api = Ltp()
    handle_request(api.call(args.text, args.pattern))
