''' TODO: 
	URL is hardcoded as localhost here - make it generic
	Separate functions for separate request types to handle data differently
	Error handling 
'''		
import urllib2
import json
import pprint
import time
import datetime
# takes the query and returns the result
def request(request_type, query, start=None, end=None, step=None):
	print "start_time is ", start
	print "end_time is ", end
	if (start!=None and end!=None):
		string = 'http://localhost:9090/api/v1/' + request_type + '?query=' + query + '&start='+start+'&end='+end + '&step=' + step
	else:
		string = 'http://localhost:9090/api/v1/' + request_type + '?query=' + query 
	print "Query string is ", string	
	response = requests.get(string)
	decoded_obj = json.loads(response.content)
	pp = pprint.PrettyPrinter(depth=6)
	pp.pprint(decoded_obj)
	result  = decoded_obj['data']['result']
	# print the JSON nicely
	pp.pprint(result)
	values = result[0]['values']
	# this segment of code will only work when querying for ranges of data, need to change
	for i in values:
		print i[1]

	print values
# testing with a particular query
query = 'cassandra_clientrequest_latency{clientrequest="ViewWrite",instance="localhost:7070",job="cassandra"}'
start1 =  strict_rfc3339.timestamp_to_rfc3339_utcoffset(time.time())
end1 =  strict_rfc3339.timestamp_to_rfc3339_utcoffset(time.time()+300)

start2 = str(time.time())
end2 = str(time.time()+300)
print "Request one"
request('query_range', query, start1, end1,'15s')
'''print "Request two"
request('query_range', query, start2, end2, '15s')
print "Request three"
request('query', query)'''

