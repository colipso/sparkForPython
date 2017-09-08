#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Thu Jul 20 21:27:37 2017

@author: hp
"""

from pymongo import MongoClient as MC
import logging
import os



class IO_mongo(object):
    def __init__(self , db = 'twitterDB' , coll = 'twitter_data' , host="localhost", port=27017):
        self.dbName = db
        self.collName = coll
        appName = 'IO_mongo'
        self.logger = logging.getLogger(appName)
        logPath = os.getcwd() + '/log'
        fileName = appName
        fileHandler = logging.FileHandler('{}/{}.log'.format(logPath , fileName))
        formatter = logging.Formatter('%(asctime)s - %(name)s -%(levelname)s - %(message)s')
        fileHandler.setFormatter(formatter)
        streamHandler = logging.StreamHandler()
        self.logger.addHandler(streamHandler)
        self.logger.addHandler(fileHandler)
        self.logger.setLevel(logging.DEBUG)
        try:
            self.client = MC(host=host, port=port)
            self.db = self.client[db]
            self.coll = self.db[coll]
            self.logger.info('Success connect to mongo database[{}]-coll[{}]'.format(db ,coll))
        except Exception as e:
            self.logger.error('Connect mongodb error : %s' % e)
            

    def __del__(self):
        self.client.close()
        
    def save(self , data_dict):
        try:
            self.coll.insert(data_dict)
            self.logger.info('Insert data into mongodb({})-table({}) success'.format(self.dbName , self.collName))
        except Exception as e:
            self.logger.error('Insert data into mongodb({})-table({}) error:{}'.format(self.dbName , self.collName , e))
        
    def load(self ,return_cursor = False , criteria = None , projection = None):
        if criteria is None:
            criteria = {}
        if projection is None:
            cursor = self.coll.find(criteria)
        else:
            cursor = self.coll.find(criteria , projection)
        
        if return_cursor:
            return cursor
        else:
            return [item for item in cursor]
        
#test
#mongoSaver = IO_mongo(db = 'twitterDB' ,  coll = 'twitter_data').save
#mongoSaver({'b':2})
#mongoSaver([{'a':1},{'b':2}])
#endtest