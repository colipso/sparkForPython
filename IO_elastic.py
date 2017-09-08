#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Thu Sep  7 15:10:55 2017

@author: hp
"""

#from elasticsearch import Elasticsearch
import json
import logging
import os
from elasticsearch import Elasticsearch
import time
import pprint
import email.utils
import datetime
import copy


class IO_elasticsearch:
    def __init__(self , index = 'feeds'):
        self.index = index
        self.es = Elasticsearch()
        
        #set logger
        #set logger
        appName = 'IO_elasticsearch'
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
    def save(self , data):
        datas = copy.deepcopy(data)
        if type(datas) == list:
            for d in datas:
                d['created_at'] = datetime.datetime.fromtimestamp(time.mktime(email.utils.parsedate(d['created_at'])))
                self.es.index(index = self.index , doc_type = 'twitter' , body = d)
        if type(datas) == dict:
            datas['created_at'] = datetime.datetime.fromtimestamp(time.mktime(email.utils.parsedate(datas['created_at'])))
            self.es.index(index = self.index , doc_type = 'twitter' , body = datas)
            
        self.logger.info('There {} records saved into elasticsearch-{}'.format(str(len(datas)) , self.index))
        
    def delIndex(self , index='feeds'):
        self.es.indices.delete(index = self.index )
        self.logger.info('Del elasticsearch index({}) success.'.format(index))
        
'''
#test
f = open('./data/twitterData.json')
datas = []
for line in f.readlines():
    d = json.loads(line.strip())
    print type(d)
    pprint.pprint( d )
    #time.sleep(10)
    datas.append(d)
    
    
#IO_elasticsearch().delIndex()
IO_elasticsearch().save(datas)
'''