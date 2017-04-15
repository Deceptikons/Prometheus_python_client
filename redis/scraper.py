#!/usr/bin/python
import requests 
import time
import redis
import tqdm
from mesosdnsclient import request
node_exporter_uri = "http://localhost:7070/metrics"
def scrape(uri, ip_address):
  try:
    page = requests.get(uri)
    timestamp = time.time()
    #print page.content
    data_lines = page.content.split("\n")
    r = redis.StrictRedis()
    for line in data_lines:
      if (line):
        # we ignore lines starting with #
        if (line[0]!='#'):
          #print line
          # format is main-attribute{key1="value1", key2... } actual value
          # we first get the entire key
          if "{" in line: 
            key,key1 = line.split("{")
            key2, value = key1.split("}")
            final_key = key +","  + key2 + ",instance_ip=" + ip_address
            r.zadd(final_key, timestamp, value)
            r.sadd("keyset", final_key)
          # Single key-value pair - can be separated by space
          else: 
            final_key,value = line.split(" ")
            final_key = final_key + ",instance_ip=" + ip_address
            r.zadd(final_key, timestamp, value)
					r.sadd("keyset", final_key)
  except:
    pass

# we print all keys
#print r.lrange("keys", 0, -1)

# this function needs to be called before scrape everytime
# returns a list of uris to hit
def init_uris(): 
	# we call mesos-dns - we hardcode IP to localhost for now
	# services are cassandra-seed and test-app for now 
	# All ports are 7070 for JMX and 9100 for node
	try:
		seed_ip = request("localhost", "cassandraseed")
		uri_list = []
		if (seed_ip[0]!=''):
			seed_uri = "http://" + seed_ip[0] + ":7070/metrics"
			uri_list.append((seed_uri,seed_ip[0]))
			# we get a list of test-app instances
			non_seed_ips = request("localhost", "test-app")
			for ip in non_seed_ips:
				if (ip!=""):
					non_seed_uri = "http://" + ip + ":7070/metrics"
					uri_list.append((non_seed_uri, ip))
	except:
		pass

	# we now add the node_exporter uris
	node_exporter_uri = "http://localhost:9100/metrics"
	uri_list.append((node_exporter_uri, '"localhost"'))
	node_exporter_uri = "http://10.10.1.72:9100/metrics"
	uri_list.append((node_exporter_uri, '"10.10.1.72"'))
	return uri_list
	


if (__name__=="__main__"):
	node_exporter_uri = "http://localhost:9100/metrics"
	for i in tqdm.tqdm(range(500000)):
		uri_to_scrape = init_uris()
		print uri_to_scrape
		for uri in uri_to_scrape:
			scrape(uri[0],uri[1])
		time.sleep(1)
	for key in r.lrange("keys", 0, -1):
		timestamp = time.time()
		print key ,": ", r.zrangebyscore(key, 0, timestamp+100001)


