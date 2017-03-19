#!/usr/bin/python
import requests
import json
import pprint
import time
import datetime
import sys
#take the name of the program and return the IP address of the service

def request(ip,service_name):
  request_string = "http://" + ip + ":8123/v1/hosts/" + service_name + ".MyMesosDockerExample.mesos"
  print request_string
  #send the request
  #print "query is ", request_string
  response = requests.get(request_string)
  array = json.loads(response.text)
  # there may be more than one address
  ip_address = []
  for element in array:
    ip_address.append(element["ip"])
  print ip_address[0]
  return ip_address
if (__name__=="__main__"):
  ip = sys.argv[1]
  query = sys.argv[2]
  request(ip, query)
