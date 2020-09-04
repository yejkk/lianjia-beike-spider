#!/usr/bin/env python
# coding=utf-8
# author: sinye
# 此代码仅供学习与交流，请勿用于商业用途。
# tor http 请求函数

import requests

def get_request():
    return get_tor_session()

def get_tor_session():
    session = requests.session()
    # Tor uses the 9050 port as the default socks port
    session.proxies = {'http':  'socks5://127.0.0.1:9050',
                       'https': 'socks5://127.0.0.1:9050'}
    return session

if __name__ == '__main__':
    pass
