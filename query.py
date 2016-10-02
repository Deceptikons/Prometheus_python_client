''' TODO: 
	URL is hardcoded as localhost here - make it generic
	Separate functions for separate request types to handle data differently
	Error handling 
'''		
import requests
import json
import pprint
import time
import datetime
# takes the query and returns the result

def request(request_type, query, start=None, end=None, step=None, logging_level=0):
	if (start!=None and end!=None and step!=None):
		string = 'http://localhost:9090/api/v1/' + request_type + '?query=' + query + '&start='+start+'&end='+end + '&step=' + step
	else:
		string = 'http://localhost:9090/api/v1/' + request_type + '?query=' + query 
	response = requests.get(string)
	decoded_obj = json.loads(response.content)
	if (logging_level>0):
		pp = pprint.PrettyPrinter(depth=6)
		pp.pprint(decoded_obj)
	result  = decoded_obj['data']['result']
	if (logging_level>0):
		# print the JSON nicely
		pp.pprint(result)
	returned_values = []# the list of values we return
	for iterable in result:
		# if the query was a range type
		if (request_type=='query_range'):
			values = iterable['values']
			for i in values:
				returned_values.append(i[1])
		elif (request_type=='query'):
			returned_values.append(iterable['value'][1])
	return returned_values


# testing with a particular query

def sendRequest(query):
	start = str(time.time())
	end = str(time.time()+300)
	return request('query', query, start, end)

