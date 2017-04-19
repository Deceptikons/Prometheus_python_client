from query import queryStats
import requests
import time
import json
import math

def throughput(ip):
  querydict= {}
  querydict["attribute"] = "org_apache_cassandra_metrics_clientrequest_count"
  stats = queryStats(querydict)
  return_list = [] 
  for stat in stats:
    # not sure which attribute it has. TODO: find out how to get just read 
    temp_dict = {}
    if (isinstance(stat, dict) and stat["scope"] == "Read" and stat["name"] == "Latency" and stat["instance_ip"] == ip):
      tuples = stat["values"]
      if (len(tuples)!=0):
        #print tuples, stat["scope"], stat["name"]
        number_of_requests = abs(float(tuples[-1][0]) - float(tuples[0][0]))/60
        temp_dict["values"] = number_of_requests
        for key in stat.keys():
          if (key!="values"):
            temp_dict[key] = stat[key]
        return_list.append(temp_dict)
  #print return_list
  return return_list

if (__name__=="__main__"):
  throughput('11.40.0.2')

