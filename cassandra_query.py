#!/usr/bin/python
''' Query Prometheus for data on
	- Threadpools 
	- Read latency
	- Write latency'''

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
overall_stats = []
def collect_stats():
	global overall_stats
	#dictionary = query.sendRequest('org_apache_cassandra_metrics_threadpools_value')
	targetdictionary = query.sendRequest('org_apache_cassandra_metrics_clientrequest_98thpercentile')
	print targetdictionary
	#overall_stats.append(LabeledPoint(targetdictionary['Read'], dictionary.values()))
answer = raw_input("use old data? (y/n)")
if (answer == 'N' or answer == 'n'):
	#for i in xrange(100):
	for i in tqdm.tqdm(range(2)):
		try:
			collect_stats()
	#		print overall_stats
			time.sleep(1)
		except KeyError:
			print "Got a keyError"
			time.sleep(1)
	new_answer = raw_input("Save the existing data\n")
	if (new_answer=='Y'):
		pickle.dump(overall_stats, open("Cassandra_stats.pkl", "w+"))
else:
	overall_stats = pickle.load(open("Cassandra_stats.pkl", "r+"))
# now that we're done with data collection, we train a regression tree using Spark

'''sc = SparkContext(appName="CassandraRegressionTree")
sqlcontext = SQLContext(sc)
data = sc.parallelize(overall_stats)
#rdf = data.toDF()
# we split the data into 70/30 
(trainingData, testData) = data.randomSplit([0.7,0.3])
print trainingData.take(2)
model = DecisionTree.trainRegressor(trainingData, categoricalFeaturesInfo={},
		impurity='variance', maxDepth=10, maxBins=32)
    
predictions = model.predict(testData.map(lambda x: x.features))
labelsAndPredictions = testData.map(lambda lp: lp.label).zip(predictions)
print labelsAndPredictions.take(30)
testMSE = labelsAndPredictions.map(lambda (v, p): (v - p) * (v - p)).sum() /\
	float(testData.count())
print ('Predictions etc - ', labelsAndPredictions)
print('Test Mean Squared Error = ' + str(testMSE))
print('Learned regression tree model:')
print(model.toDebugString())
'''
