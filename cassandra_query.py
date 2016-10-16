#!/usr/bin/python
''' Query Prometheus for data on
	- Threadpools 
	- Read latency
	- Write latency'''

import query
import time
# we periodically send this request every 10(?) seconds 
overall_stats = []
def collect_stats():
	global overall_stats
	overall_stats.append(query.sendRequest('org_apache_cassandra_metrics_threadpools_value') +\
			query.sendRequest('org_apache_cassandra_metrics_clientrequest_98thpercentile'))

for i in range(0,100):
	collect_stats()
	print overall_stats
	time.sleep(10)
	

