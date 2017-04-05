from query import queryStats
import requests

# we query for idle stats
def analysis():
	querydict= {}
	querydict["attribute"] = "node_cpu"
	stats = queryStats(querydict)
	print stats
	global_avg=0
	cpu_count=0
	# we look for idle time
	for stat in stats:
		if (isinstance(stat, dict) and 'mode' in stat.keys() and stat['mode'] == "idle"):
			# we now calculate the average of the list of values
			tuples = stat["values"]
			# we calculate the percentage of utilization 
			if (len(tuples)!=0):
				time_taken = float(tuples[-1][1]) - float(tuples[0][1])
				cpu_time = float(tuples[-1][0]) - float(tuples[0][0])
				avg = 100- (cpu_time/time_taken*100)
				print "average utilization ", avg
				global_avg+=avg
				cpu_count+=1
	# now we can compute average utilization across all cpus
	if (cpu_count!=0):
		global_avg/=cpu_count
	print global_avg
	# if the utilization is >70% we can do some scaling up
	# if it is less than 10% we can do some scaling down
	if (global_avg<10):
		# we scale_down
		r = requests.post("http://localhost:5000/status", data={"state": "down"})
		print (r.status_code, r.reason)
	elif (global_avg>70):
		r = requests.post("http://localhost:5000/status", data={"state": "up"})
		print (r.status_code, r.reason)
		
analysis()
