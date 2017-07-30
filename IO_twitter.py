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
import logging
import os

import config
consumer_key = config.consumer_key
consumer_secret = config.consumer_secret
access_token = config.access_token
access_secret = config.access_secret

import IO
import IO_mongodb
#access Internet by VPN
import socks
import socket
defaultConn = socket.socket
if config.VPN:
    socks.setdefaultproxy(socks.PROXY_TYPE_SOCKS5, "127.0.0.1", 1080)
    proxy = socks.socksocket
    socket.socket = proxy
    def getaddrinfo(*args):
        return [(socket.AF_INET, socket.SOCK_STREAM, 6, '', (args[0], args[1]))]
    socket.getaddrinfo = getaddrinfo



class TwitterAPI(object):
    def __init__(self):
        #set logger
        appName = 'TwitterAPI'
        self.logger = logging.getLogger(appName)
        logPath = os.getcwd() + '/log'
        fileName = appName
        fileHandler = logging.FileHandler('{}/{}.log'.format(logPath , fileName))
        streamHandler = logging.StreamHandler()
        formatter = logging.Formatter('%(asctime)s - %(name)s -%(levelname)s - %(message)s')
        fileHandler.setFormatter(formatter)
        self.logger.addHandler(fileHandler)
        self.logger.addHandler(streamHandler)
        self.logger.setLevel(logging.DEBUG)
        
        #access to twitter
        self.consumer_key = consumer_key
        self.consumer_secret = consumer_secret
        self.access_token = access_token
        self.access_secret = access_secret
        try:
            self.api = twitter.Api(access_token_key = self.access_token,
                               access_token_secret = self.access_secret,
                               consumer_key = self.consumer_key,
                               consumer_secret = self.consumer_secret)
            self.logger.info('TwitterAPI get access to twitter')
        except Exception as e:
            self.logger.error('Error when access twitter api : %s' % e)
        self.retries = 3
        
        #json Saver
        jsonPath = os.getcwd() + '/data'
        jsonFname = 'twitterData'
        ioJson = IO.IO_json(jsonPath , jsonFname)
        self.jsonSaver = ioJson.save
        
        #mongo Saver
        self.mongoSaver  = IO_mongodb.IO_mongo(db = 'twitterDB' ,  coll = 'twitter_data').save
        
        self.logger.info('TwitterAPI init completed')
        
    def __del__(self):
        del(self.mongoSaver)
        del(self.jsonSaver)
        del(self.api)
        del(self.logger)
        
    def searchTwitter(self , q , max_res = 20 , **kwargs):
        socket.socket = proxy
        query = 'q=' + quote(q) + '&src=typd'
        search_result = self.api.GetSearch(raw_query = query , count = max_res)
        self.logger.info('Get {} resourses by searchTwitter({})'.format(str(max_res) , str(q)))
        result = [s.AsDict() for s in search_result]
        self.saveTweets(result)
        return result
    
    def getTwitter(self , userScreenName , max_res = 20 , **kwargs):
        socket.socket = proxy
        statuses = self.api.GetUserTimeline(screen_name = userScreenName , count = max_res)
        #pprint(statuses)
        result = [s.AsDict() for s in statuses]
        self.saveTweets(result)
        return result
    
    def saveTweets(self ,statuses):
        socket.socket = defaultConn
        if type(statuses) == list:
            for s in statuses:
                self.jsonSaver(s)
        elif type(statuses) == dict:
            self.jsonSaver(statuses)
        else:
            self.logger.error('The structure of data to save is wrong')
            return False
        

        self.mongoSaver(statuses)
    
    def parseTweets(self , statuses):
        '''
        '''
        return [(s['id'] , 
                 s['created_at'] , 
                 s['user']['id'] , 
                 s['user']['name'] ,
                 s['text'] , 
                 u['expanded_url']) 
                    for s in statuses
                        for u in s['urls']]

''' 
#test
TAPI = TwitterAPI()
result = TAPI.searchTwitter('happy new year')
print '================================'

result2= TAPI.getTwitter('Arthur')

#endtest
'''