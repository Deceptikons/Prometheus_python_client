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
# if the query is from jmx exporter the format is [data][result][metric][scope]
# for metadata and [data][result][value][1] fo hte data
# if the query is for a stat from node_exporter the format is
# [data][result][metric] gives an object for the metadata
def request(request_type, query, start=None, end=None, step=None, logging_level=0, source_type="node_hybrid"):
  if (start!=None and end!=None and step!=None):
    string = 'http://localhost:9090/api/v1/' + request_type + '?query=' + query + '&start='+start+'&end='+end + '&step=' + step
  else:
    string = 'http://localhost:9090/api/v1/' + request_type + '?query=' + query 
  response = requests.get(string)
  decoded_obj = json.loads(response.content)
  if (logging_level==2):
    pp = pprint.PrettyPrinter(depth=6)
    pp.pprint(decoded_obj)
  result  = decoded_obj['data']['result']
  if (logging_level==2):
    # print the JSON nicely
    pp.pprint(result)
  returned_values = {}# the dictionary of values we return
  for iterable in result:
    if (source_type=="jmx"):
      # if the query was a range type
      if (request_type=='query_range'):
        values = iterable['values']
        for i in values:
          returned_values[iterable['metric']['scope']]=float(i[1])
      elif (request_type=='query'):
        returned_values[iterable['metric']['scope']]=float(iterable['value'][1])
    elif (source_type=="node_atomic"):
      # assuming query is not a range type here
      # build the key
      key=iterable['metric']['instance']+iterable['metric']['cpu']+ iterable['metric']['mode']
      returned_values[key]=float(iterable['value'][1])
    elif (source_type=="node_hybrid"):
      key=iterable['metric']['instance']
      print key
      returned_values[key]=float(iterable['value'][1])
    if (logging_level==1):
      print returned_values
    return returned_values


# testing with a particular query

def sendRequest(query):
  start = str(time.time())
  end = str(time.time()+300)
  return request('query', query, start, end,logging_level=1)

