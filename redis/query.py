#!/usr/bin/python
import redis
import time

# In the web service, this should be created only once,
#	not for every request
r = redis.StrictRedis()

# The query should be a dictionary/JSON passed 
# it should contain two key-value pairs - query and the instance
def queryStats(querydict):
	# we first get all the keys
	key_list = r.smembers("keyset")
	#print key_list
	keys_to_query = set()
	# we build hashes for each key
	for key in key_list:
		hashes = {}
		if (querydict["attribute"] in key):
			if ("instance" in querydict.keys() and querydict["instance"] in key):
				keys_to_query.add(key)
			elif ("mode" in querydict.keys() and querydict["mode"] in key):
				keys_to_query.add(key)
			else:
				keys_to_query.add(key)
	#print keys_to_query
	# we query for all these keys now. We split the key into the following
	# query - the part before the first ','
	# split all the other key-value pairs using '='
	return_dict= []
	for key in keys_to_query:
		temp_dict = {}
		pairs = key.split(",")
		temp_dict["query"] = pairs[0] 
		for pair in pairs[1:]:
			innerpair = pair.split("=")
			#print	innerpair 
			if (len(innerpair)==2):
				if innerpair[1].startswith('"') and innerpair[1].endswith('"'):
					innerpair[1]= innerpair[1][1:-1] 
				temp_dict[innerpair[0]] = innerpair[1]
		# Finally we query. We return values from the last hour
		timestamp = time.time()
		values = r.zrangebyscore(key,timestamp-60, timestamp,withscores=True )
		temp_dict["values"] = values
		return_dict.append(temp_dict)
		#print temp_dict
	return return_dict

if (__name__=="__main__"):
	# test for this
	print "hello"
	querydict = {}
	querydict["attribute"] = "org_apache_cassandra_metrics_clientrequest_98thpercentile"
	print queryStats(querydict)
'''

	querydict = {}
	querydict["attribute"] = "org_apache_cassandra_metrics_clientrequest_count"
	print queryStats(querydict)
'''
