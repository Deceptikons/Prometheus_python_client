from query import queryStats
import requests
import json

keys = {}


def formatter(a):
	res = []
	for i in a:
		x = i
		x_axis = i[1]
		y_axis = float(i[0][1:])
		x = [x_axis,y_axis]
		res.append(x)
	return res


def initialize():	
	querydict= {}
	querydict["attribute"] = "node_cpu"
	stats = queryStats(querydict)
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

def idleStats(cpu):
	querydict= {}
	querydict["attribute"] = "node_cpu"
	stats = queryStats(querydict)
	#for stat in stats:	
	#print stats
	return keys["idle"]
