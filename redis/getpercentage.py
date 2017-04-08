from query import queryStats

''' This function will take the querydictionary, return a 
		list of dictionaries with a list of percentage points '''

def return_percentage_points(querydict):
	# first we get the stats from queryStats function
	stats = queryStats(querydict)
	# for debug purposes we print 
	print stats
	# we iterate over the list of values
	return_dict = []
	for stat in stats:
		temp_dict = {}
		# we init the dictionary with the same k-v pairs 
		for key in stat.keys():
			if (key!="values"):
				temp_dict[key] = stat[key]
			else: 
				# we replace values with percentage points
				temp_dict["values"] = []
				values = stat["values"]
				for index in range(len(values)-2):
					stat_diff = float(values[index+1][0]) - float(values[index][0])
					time_diff = float(values[index+1][1]) - float(values[index][1])
					percentage = (stat_diff/time_diff) * 100
					temp_dict["values"].append(percentage)
		# at this stage temp_dict is initialized 
		# we can add it to return_dict
		print temp_dict
		return_dict.append(temp_dict)
	return return_dict

if (__name__=="__main__"):
	querydict = {}
	querydict["attribute"] = "node_cpu"
	result = return_percentage_points(querydict)
	#print result


					
					


