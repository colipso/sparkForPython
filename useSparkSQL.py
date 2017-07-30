#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Mon Jul 24 15:46:16 2017

@author: hp
"""
mongo = False
import os
from pyspark import SparkConf , SparkContext
from pyspark.sql import SparkSession , Row 

'''
sc = SparkContext("local[4]" , "useSparkSQL")
sc.setLogLevel("ERROR")
sqlc = SQLContext(sc)

dataPath = os.getcwd() + '/data'
print '{}/{}.json'.format(dataPath , 'twitterData')
twts_sql_df_01 = sqlc.read.json('{}/{}.json'.format(dataPath , 'twitterData'))

twts_sql_df_01.show(
'''
#use sparksession to replace sparkcontext

spark = SparkSession \
                    .builder \
                    .appName('useSparkSQL') \
                    .config('spark.mongodb.input.uri','mongodb://127.0.0.1/twitterDB.twitter_data') \
                    .config('spark.mongodb.output.uri','mongodb://127.0.0.1/twitterDB.twitter_data') \
                    .getOrCreate()
                    
#IF programme want access to mongo ,it should start up by 
# spark-submit --packages org.mongodb.spark:mongo-spark-connector_2.11:2.1.0 useSparkSQL.py

if mongo:
    print '=============Data loaded from mongo'
    twts_sql_df_mongo = spark.read.format("com.mongodb.spark.sql.DefaultSource").load()
    twts_sql_df_mongo.show()
    twts_sql_df_mongo.printSchema()

dataPath = os.getcwd() + '/data'
twts_sql_df_01 = spark.read.json('{}/{}.json'.format(dataPath , 'twitterData'))
#twts_sql_df_01.show()
twts_sql_df_01.printSchema()
twts_sql_df_01.select('user.name').show()

twts_sql_df_01.registerTempTable('tweets_01')
twts_sql_df_01_selection = spark.sql("select user.lang from tweets_01 where user.name= 'Jhake'")
twts_sql_df_01_selection.explain(True)
twts_sql_df_01_selection.show()

twts_sql_df_csv = spark.read.csv('{}/{}.csv'.format(dataPath , 'csvData'),header=True)
twts_sql_df_csv.printSchema()
twts_sql_df_csv.columns
twts_sql_df_csv.show()