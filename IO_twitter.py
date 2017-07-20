#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Wed Jul 19 20:10:51 2017

@author: hp
"""

import twitter # pip install python-twitter
import urlparse
from pprint import pprint
from urllib import quote

import config
consumer_key = config.consumer_key
consumer_secret = config.consumer_secret
access_token = config.access_token
access_secret = config.access_secret

#access Internet by VPN
if config.VPN:
    import socks
    import socket
    socks.setdefaultproxy(socks.PROXY_TYPE_SOCKS5, "127.0.0.1", 1080)
    socket.socket = socks.socksocket
    def getaddrinfo(*args):
        return [(socket.AF_INET, socket.SOCK_STREAM, 6, '', (args[0], args[1]))]
    socket.getaddrinfo = getaddrinfo


class TwitterAPI(object):
    def __init__(self):
        self.consumer_key = consumer_key
        self.consumer_secret = consumer_secret
        self.access_token = access_token
        self.access_secret = access_secret
        self.api = twitter.Api(access_token_key = self.access_token,
                               access_token_secret = self.access_secret,
                               consumer_key = self.consumer_key,
                               consumer_secret = self.consumer_secret)
    def searchTwitter(self , q , max_res = 20 , **kwargs):
        query = 'q=' + quote(q) + '&src=typd' 
        search_result = self.api.GetSearch(raw_query = query , count = max_res)
        #pprint(search_result)
        #print type(search_result[0])
        return [s.AsDict() for s in search_result]
    def getTwitter(self , userScreenName , max_res = 20 , **kwargs):
        statuses = self.api.GetUserTimeline(screen_name = userScreenName , count = max_res)
        #pprint(statuses)
        return [s.AsDict() for s in statuses]
    

        
        
        
        
#test
#result = TwitterAPI().getTwitter('misscrybby')
#pprint(result)
result = TwitterAPI().searchTwitter('happy new year')
pprint(result)
#endtest
