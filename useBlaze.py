#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Mon Jul 24 12:52:21 2017

@author: hp
"""

import numpy as np
import pandas as pd
from blaze import Data , by , join , merge
from odo import odo
import os
import IO_twitter
#set logger
import logging
appName = 'useBlaze'
logger = logging.getLogger(appName)
logger.setLevel(logging.DEBUG)
logPath = os.getcwd() + '/log'
fileName = appName
fileHandler = logging.FileHandler('{}/{}.log'.format(logPath , fileName))
formatter = logging.Formatter('%(asctime)s -- %(name)s -- %(levelname)s -- %(message)s')
fileHandler.setFormatter(formatter)
logger.addHandler(fileHandler)
streamHandler = logging.StreamHandler()
logger.addHandler(streamHandler)

import IO

dataPath = os.getcwd() + '/data'

twts_data = IO.IO_json(dataPath , 'twitterData').load()
logger.debug('Type of loaded json is %s' %str(type(twts_data)))
twts_read = IO_twitter.TwitterAPI().parseTweets(twts_data)

fields =  ['id', 'created_at', 'user_id', 'user_name', 'tweet_text', 'url']

twts_pd_df = pd.DataFrame(twts_read , columns = fields)

twts_pd_df.head()
twts_pd_df.describe()

twts_bz_df = Data(twts_pd_df)

twts_bz_df.schema
twts_bz_df.dshape

twts_bz_df.data

tweet_text_distinct = twts_bz_df.tweet_text.distinct()
tweet_text_distinct

twts_bz_df[['id' , 'user_name' , 'tweet_text']].distinct()


twts_odo_df = Data(twts_pd_df)
print twts_odo_df.dshape

odo(twts_bz_df , 'jsonlines://{}/{}.json'.format(dataPath , 'jsonData'))

print '====================='
odo(twts_bz_df, '{}/{}.csv'.format(dataPath , 'csvData'))


