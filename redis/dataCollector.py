from query import queryStats
import requests
import json
from getpercentage import return_percentage_points
keys = {}
keys_latency = {}
memory = {}
def formatter_util(a):
	res = []
        count = 0
	for i in a:
		x = i
		x_axis = count
		count+=1
		y_axis = i
		res.append([x_axis,y_axis])
	return res
def formatter_latency(a):
	res = []
	count = 0
	for i in a:
		x = i
		x_axis = count
		count+=1
		y_axis = float(i[0][1:])
		res.append([x_axis,y_axis])
	return res
 
def formatter(a):
	res = []
	print a
	for i in a:
		x = i
		x_axis = i[1]
		y_axis = float(i[0][1:])
		x = [x_axis,y_axis]
		res.append(x)
	return res

def memoryFree():
	querydict = {}
	querydict["attribute"] = "node_memory_MemTotal"
	stats = queryStats(querydict)
	for stat in stats:
		stat["values"] = formatter_util(stat["values"])
		print stat
                #print stat['mode']
                if stat["instance_ip"] not in memory :
                        memory.update({stat["instance_ip"] : { stat["query"] : stat["values"] } })
                elif stat["instance_ip"] != None:
                        print " !!!!@@@@!!!!" , stat["instance_ip"]
                        print " %%%%%%%%%%% " , memory[stat["instance_ip"]]
                        if memory[stat["instance_ip"]] != None:
                                #print " (((())))) ",stat["scope"] , stat["values"]
                                temp = memory[stat["instance_ip"]]
                                temp.update({stat["query"]:stat["values"]})
                                print "AFTER ",temp
                                memory[stat["instance_ip"]] = temp
                                print "......................... ",memory[stat["instance_ip"]]
	querydict = {}
	querydict["attribute"] = "node_memory_MemFree"
	stats = queryStats(querydict)
	for stat in stats:
		stat["values"] = formatter_util(stat["values"])
		if(stat["instance_ip"] not in memory):
			memory.update({stat["instance_ip"] : { stat["query"] : stat["values"] }})
		elif stat["instance_ip"]!=None:
			print " !!!!@@@@!!!!" , stat["instance_ip"]
                        print " %%%%%%%%%%% " , memory[stat["instance_ip"]]
                        if memory[stat["instance_ip"]] != None:
                                #print " (((())))) ",stat["scope"] , stat["values"]
                                temp = memory[stat["instance_ip"]]
                                temp.update({stat["query"]:stat["values"]})
                                print "AFTER ",temp
                                memory[stat["instance_ip"]] = temp
                                print "......................... ",memory[stat["instance_ip"]]

	print "MEM !! : ",memory
	return memory

def initialize_util(ip):
	
	querydict= {}
	querydict["attribute"] = "node_cpu"
	#stats = queryStats(querydict)
	stats = return_percentage_points(querydict)
	print "STATS :",stats
	for stat in stats:
		stat["values"] = formatter_util(stat["values"])
		print "***************************************************************"
		print stat
		#print stat['mode']
		if stat["mode"] not in keys and stat["instance_ip"] == ip:
			keys.update({stat["mode"] : { stat["cpu"] : stat["values"] } })
		elif stat["mode"] != None and stat["instance_ip"] == ip:
			print " !!!!@@@@!!!!" , stat["mode"]
			print " %%%%%%%%%%% " , keys[stat["mode"]]
			if keys[stat["mode"]] != None:
				print " (((())))) ",stat["cpu"] , stat["values"]
				temp = keys[stat["mode"]]
				temp.update({stat["cpu"]:stat["values"]})
				print "AFTER ",temp
				keys[stat["mode"]] = temp
				print "......................... ",keys[stat["mode"]]
	print " >>>> > >>> >>>>>",keys

def initialize():	
	querydict= {}
	querydict["attribute"] = "node_cpu"
	#stats = queryStats(querydict)
	stats = return_percentage_points(querydict)
	for stat in stats:
		stat["values"] = formatter(stat["values"])
		print "***************************************************************"
		print stat
		#print stat['mode']
		if stat["mode"] not in keys :
			keys.update({stat["mode"] : { stat["cpu"] : stat["values"] } })
		elif stat["mode"] != None:
			print " !!!!@@@@!!!!" , stat["mode"]
			print " %%%%%%%%%%% " , keys[stat["mode"]]
			if keys[stat["mode"]] != None:
				print " (((())))) ",stat["cpu"] , stat["values"]
				temp = keys[stat["mode"]]
				temp.update({stat["cpu"]:stat["values"]})
				print "AFTER ",temp
				keys[stat["mode"]] = temp
				print "......................... ",keys[stat["mode"]]
	print " >>>> > >>> >>>>>",keys

def idleStats(cpu,ip):
	querydict= {}
	querydict["attribute"] = "node_cpu"
	stats = queryStats(querydict)
	#for stat in stats:	
	#print stats
	return keys["idle"]

def getLatency():
	querydict={}
	querydict["attribute"] = "org_apache_cassandra_metrics_clientrequest_98thpercentile"
	stats = queryStats(querydict)
	for stat in stats:
		stat["values"] = formatter_latency(stat["values"])
		print "***************************************************************"
		print stat
		#print stat['mode']
		if stat["instance_ip"] not in keys_latency :
			keys_latency.update({stat["instance_ip"] : { stat["scope"] : stat["values"] } })
		elif stat["instance_ip"] != None:
			print " !!!!@@@@!!!!" , stat["instance_ip"]
			print " %%%%%%%%%%% " , keys_latency[stat["instance_ip"]]
			if keys_latency[stat["instance_ip"]] != None:
				print " (((())))) ",stat["scope"] , stat["values"]
				temp = keys_latency[stat["instance_ip"]]
				temp.update({stat["scope"]:stat["values"]})
				print "AFTER ",temp
				keys_latency[stat["instance_ip"]] = temp
				print "......................... ",keys_latency[stat["instance_ip"]]
	return keys_latency
	#return "SUCCESS"
def computeCPU(host):
	querydict={}
	querydict["attribute"] = "node_cpu"
	querydict["mode"] = "idle"
	stats = queryStats(querydict)
	cpu_count = 0
	global_avg = 0
	cpu_utils=[]
	print stats
	for stat in stats:
		print stat["instance_ip"],"    ",host
                if (isinstance(stat, dict) and 'mode' in stat.keys() and stat['mode'] == "idle" and stat["instance_ip"] == host):
                        # we now calculate the average of the list of values
                        tuples = stat["values"]
                        # we calculate the percentage of utilization 
                        if (len(tuples)!=0):
                                time_taken = float(tuples[-1][1]) - float(tuples[0][1])
                                cpu_time = float(tuples[-1][0]) - float(tuples[0][0])
                                avg = 100- (cpu_time/time_taken*100)
                                print "average utilization ", avg
				cpu_utils.append(avg)
                                global_avg+=avg
                                cpu_count+=1
	print " GLOBAL :",global_avg/cpu_count
	return global_avg/cpu_count


if (__name__ == "__main__"):
	memoryFree()
