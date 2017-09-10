#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Fri Sep  8 20:01:32 2017

@author: hp
"""

import IO_twitter
import time
import random
import logging
import os
#set logger

appName = 'TwitterCrawler'
logger = logging.getLogger(appName)
logPath = os.getcwd() + '/log'
fileName = appName
fileHandler = logging.FileHandler('{}/{}.log'.format(logPath , fileName))
streamHandler = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s - %(name)s -%(levelname)s - %(message)s')
fileHandler.setFormatter(formatter)
logger.addHandler(fileHandler)
logger.addHandler(streamHandler)
logger.setLevel(logging.DEBUG)

twitter = IO_twitter.TwitterAPI()
words = []

wordFile = os.getcwd() + '/data/starwar.txt'
f = open(wordFile , 'r')
for line in f.readlines():
    w = line.strip().split(' ')
    words.extend(w)
f.close()
distinctWords = list(set(words))
for w in words:
    try:
        logger.info('============= \n Begin get twitter by word {}'.format(w))
        twitter.getTwitter(w)
        freezTime = random.random()
        time.sleep(freezTime)
    except:
        continue





