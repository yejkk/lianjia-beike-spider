#!/usr/bin/env python
# coding=utf-8
# author: sinye
# 此代码仅供学习与交流，请勿用于商业用途。
# tor http 请求函数

import requests
from stem import Signal
from stem.control import Controller

def get_request():
    return get_tor_session()

def get_tor_session():
    renew_connection()
    session = requests.session()
    # Tor uses the 9050 port as the default socks port
    session.proxies = {'http':  'socks5://127.0.0.1:9050',
                       'https': 'socks5://127.0.0.1:9050'}
    return session

# signal TOR for a new connection 
def renew_connection():
    with Controller.from_port(port = 9051) as controller:
        controller.authenticate(password="password")
        controller.signal(Signal.NEWNYM)

if __name__ == '__main__':
    pass
