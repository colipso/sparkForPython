#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Thu Jul 20 19:38:56 2017

@author: hp
"""

from collections import namedtuple
import os
import csv
import io
import json
import logging


class IO_csv(object):
    def __init__(self , filepath , filename , filesuffix = 'csv'):
        appName = 'IO_csv'
        self.logger = logging.getLogger(appName)
        logPath = os.getcwd() + '/log'
        fileName = appName
        fileHandler = logging.FileHandler('{}/{}.log'.format(logPath , fileName))
        formatter = logging.Formatter('%(asctime)s - %(name)s -%(levelname)s - %(message)s')
        fileHandler.setFormatter(formatter)
        self.logger.addHandler(fileHandler)
        self.logger.setLevel(logging.DEBUG)
        streamHandler = logging.StreamHandler()
        self.logger.addHandler(streamHandler)
        
        self.filePath = filepath
        self.fineName = filename
        self.fileSuffix = filesuffix
    def save(self , data , NTname , fields):
        '''
        @fields : header of csv
        '''
        NTuple = namedtuple(NTname , fields)
        dataFile = '{0}/{1}.{2}'.format(self.filePath , self.fineName , self.fileSuffix)
        if os.path.isfile(dataFile):
            with open(dataFile , 'ab') as f:
                writer = csv.writer(f)
                writer.writerows([row for row in map(NTuple._make , data)])
        else:
            with open(dataFile , 'wb') as f:
                writer = csv.writer(f)
                writer.writerow(fields)
                writer.writerows([row for row in map(NTuple._make , data)])
    def load(self , NTname , fields):
        NTuple = namedtuple(NTname , fields)
        dataFile = '{0}/{1}.{2}'.format(self.filePath , self.fineName , self.fileSuffix)
        with open(dataFile) as f:
            reader = csv.reader(f)
            for row in map(NTuple._make , reader):
                yield row
                
                
class IO_json(object):
    def __init__(self , filepath , filename , filesuffix = 'json'):
        appName = 'IO_json'
        self.logger = logging.getLogger(appName)
        logPath = os.getcwd() + '/log'
        fileName = appName
        fileHandler = logging.FileHandler('{}/{}.log'.format(logPath , fileName))
        formatter = logging.Formatter('%(asctime)s - %(name)s -%(levelname)s - %(message)s')
        fileHandler.setFormatter(formatter)
        self.logger.addHandler(fileHandler)
        self.logger.setLevel(logging.DEBUG)
        streamHandler = logging.StreamHandler()
        self.logger.addHandler(streamHandler)
        
        self.filePath = filepath
        self.fileName = filename
        self.fileSuffix = filesuffix
        
    def save(self ,data):
        dataFile = '{0}/{1}.{2}'.format(self.filePath , self.fileName , self.fileSuffix)
        if os.path.isfile(dataFile):
            with io.open(dataFile , 'a' ,encoding = 'utf-8') as f:
                f.write(unicode('\n'))
                f.write(unicode(json.dumps(data , ensure_ascii=False)))
                
        else:
            with io.open(dataFile , 'w',encoding = 'utf-8') as f:
                f.write(unicode(json.dumps(data , ensure_ascii = False)))
        self.logger.info('Saved data to %s' % dataFile)
    def load(self):
        dataFile = '{0}/{1}.{2}'.format(self.filePath , self.fileName , self.fileSuffix)
        returnData = []
        with io.open( dataFile , encoding = 'utf-8') as f:
            for line in  f.readlines():
                returnData.append(json.loads(line))
        return returnData
            

            
            
            
