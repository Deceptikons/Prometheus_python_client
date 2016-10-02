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
	overall_stats.append(query.sendRequest('cassandra_threadpools_activetasks') +\
			query.sendRequest('cassandra_clientrequest_totallatency'))

for i in range(0,100):
	collect_stats()
	print overall_stats
	time.sleep(10)
	

