#!/usr/bin/python
import requests
import json
import pprint
import time
import datetime
import sys
#take the name of the program and return the IP address of the service

def request(ip,service_name):
	request_string = "http://" + ip + ":8123/v1/hosts/" + service_name + ".marathon.mesos"
	#send the request
	#print "query is ", request_string
	response = requests.get(request_string)
	array = json.loads(response.text)
	ip_address = array[0]["ip"]

	print ip_address

ip = sys.argv[1]
query = sys.argv[2]
request(ip, query)
