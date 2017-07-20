#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Thu Jul 20 21:27:37 2017

@author: hp
"""

from pymongo import MongoClient as MC

class IO_mongo(object):
    def __init__(self , db = 'twitter_db' , coll = 'twitter_coll' , **conn):
        self.client = MC(**conn)
        self.db = self.client[db]
        self.coll = self.db[coll]
        
    def save(self , data):
        return self.coll.insert(data)
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