#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Thu May 11 14:56:17 2017

@author: hp
"""

import sys
reload(sys)
sys.setdefaultencoding('utf-8')

from os import path
import jieba
from pyspark import SparkContext
from pyspark.sql import SQLContext
from pyspark.sql.functions import length
#from operator import add

sc = SparkContext("local[1]" , "wordCount")
sc.setLogLevel("ERROR")
sqc = SQLContext(sc)

thisDir = path.dirname(__file__)

def wordCut(strings):
    strings = strings.strip()
    returnList = []
    for r in jieba.cut(strings):
        returnList.append(r)
    return returnList

fileName = 'words.txt'
file_in = sc.textFile(path.join(thisDir,fileName))

linesNum = file_in.count()
print '[INFO]number of lines in file %s : %d' % (fileName , linesNum)

charsNum = file_in.map(lambda x : len(x)).reduce(lambda x,y : x+y)
print '[INFO]number of charts in file %s : %d' % (fileName , charsNum)

words = file_in.flatMap(lambda line : wordCut(line))
termBigger3 = words.filter(lambda word : len(word) > 3)
print '[INFO]number of words bigger than 3 in file %s : %d' % (fileName , termBigger3.count())

wordCount = words.map(lambda w : (w,1)).reduceByKey(lambda x,y:x+y)
sqc.createDataFrame(wordCount,['word','count']).filter(length('word') >= 2).sort('count',ascending = False).show(20)