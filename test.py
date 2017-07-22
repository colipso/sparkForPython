#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Sat Jul 22 19:48:51 2017

@author: hp
"""

import IO_mongodb

VPN = True
if VPN:
    import socks
    import socket
    socks.setdefaultproxy(socks.PROXY_TYPE_SOCKS5, "127.0.0.2", 1080)
    socket.socket = socks.socksocket
    def getaddrinfo(*args):
        return [(socket.AF_INET, socket.SOCK_STREAM, 6, '', (args[0], args[1]))]
    socket.getaddrinfo = getaddrinfo
    

class test:
    def __init__(self):
        self.saver = IO_mongodb.IO_mongo(db = 'twitterDB' ,  coll = 'twitter_data').save

    def run(self , data):
        self.saver(data)
        
data = [{'a':1},{'b':2}]


T = test()
T.run(data)
