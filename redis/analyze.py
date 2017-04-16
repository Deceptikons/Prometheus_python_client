from query import queryStats
import requests
import time
import json

# we query for idle stats
def analysis():
	querydict= {}
	querydict["attribute"] = "node_cpu"
	querydict["mode"]= "idle"
	stats = queryStats(querydict)
	global_avg={}
	cpu_count={}
	# we look for idle time
	for stat in stats:
		if (isinstance(stat, dict) and 'mode' in stat.keys() and stat['mode'] == "idle"):
			# we now calculate the average of the list of values
			tuples = stat["values"]
			# we calculate the percentage of utilization 
			print tuples
			if (len(tuples)!=0):
				time_taken = float(tuples[-1][1]) - float(tuples[0][1])
				cpu_time = float(tuples[-1][0]) - float(tuples[0][0])
				avg = 100- (cpu_time/time_taken*100)
				print "average utilization ", avg
				if (stat["instance_ip"] not in global_avg.keys()):
					global_avg[stat["instance_ip"]]=0
					cpu_count[stat["instance_ip"]]=0
				global_avg[stat["instance_ip"]]+=avg
				cpu_count[stat["instance_ip"]]+=1
	# now we can compute average utilization across all cpus
	for key in global_avg.keys():
		if (cpu_count!=0):
			global_avg[key]/=cpu_count[key]
		print global_avg[key]
	# if the utilization is >70% we can do some scaling up
	# if it is less than 10% we can do some scaling down
	scaled=0
	for key in global_avg.keys():
		if (global_avg[key]>60):
			print "scaling up"
			data={'state': 'up'}
			r = requests.post("http://10.10.1.71:5000/status", data=json.dumps(data), headers = {'Content-Type': 'application/json'})
			print (r.status_code, r.reason)
			scaled=1
			break
		elif (global_avg[key]>30):
			print "util is ", global_avg[key]
			scaled=-1
	if (scaled==0):
		# we scale_down
		print "scaling down"
		data={'state': 'down'}
		r = requests.post("http://10.10.1.71:5000/status", data=json.dumps(data), headers = {'Content-Type': 'application/json'})
		print (r.status_code, r.reason)
if (__name__=='__main__'):
	while (True):
		analysis()
		time.sleep(30)
