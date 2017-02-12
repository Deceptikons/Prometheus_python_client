#!/usr/bin/python
import query
import tqdm
import time
import pickle
'''from pyspark import SparkContext
from pyspark.mllib.tree import DecisionTree, DecisionTreeModel
from pyspark.mllib.util import MLUtils
from pyspark.sql import SQLContext 
from pyspark.mllib.regression import LabeledPoint'''
# we periodically send this request every 10(?) seconds 
overall_stats = {}
# Name of all the stats we want to query prometheus for
stats_name_list = ["node_cpu"] 
def collect_stats():
	global overall_stats
	for i in overall_stats.keys():
		dictionary = query.sendRequest(i)
		print dictionary

def init():
	global stats_name_list
	global overall_stats
	for name in stats_name_list:
		overall_stats[name] = {}

init()
for i in tqdm.tqdm(range(1000)):
	collect_stats()
