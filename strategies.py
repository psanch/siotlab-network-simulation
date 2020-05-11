"""Implements various strategies for associating IOTs to APs. Implement yours here."""

def round_robin(w) -> bool:
	"""Implements a round-robin association strategy where iots are associated their ssid modulo number of APs.

	Return:
	Returns true on successful association. False otherwise.
	"""

	m = len(w.aps)
	i = 0

	for device in w.iots:
		if device.do_associate(w.aps[i%m]) == False:
			return False
		i += 1
	return True

def greedy_rssi(w) -> bool:
	"""Implements a greedy approach using RSSI (1/euclidean distance) as the heuristic.

	Return:
	Returns true on successful association. False otherwise.
	"""

	for device in w.iots:
		# Process the aps for validity and sort them by RSSI (bigger is better)
		valid_aps = device.get_candidate_aps(w.aps)
		distances = device.get_rssi_to_aps(valid_aps)
		distances.sort(reverse=True, key = lambda x: x[0])

		i = 0
		num_aps = len(w.aps)
		while i < num_aps:
			if (device.do_associate(distances[i][1])) == True:
				break
			else:
				i+=1
		else:
			return False
	return True

def greedy_demand_weighted_rssi(w) -> bool:
	"""Implements a greedy approach, with a-priori sorting by IOT demand.

	Return:
	Returns true on successful association. False otherwise.
	"""

	w.iots.sort(key=lambda x: x.demand, reverse=True)

	for device in w.iots:
		# Process the aps for validity and sort them by RSSI (bigger is better)
		valid_aps = device.get_candidate_aps(w.aps)
		distances = device.get_rssi_to_aps(valid_aps)
		distances.sort(reverse=True, key = lambda x: x[0])

		i = 0
		num_aps = len(distances)
		while i < num_aps:
			if (device.do_associate(distances[i][1])) == True:
				break
			else:
				i+=1
		else:
			return False
	return True

def greedy_edge_based(w) -> bool:
	"""Implements a greedy approach considering the priority of edges instead of vertices.

	Return:
	Returns true on successful association. False otherwise.
	"""

	# Setup the list of edges and sort them by edge_priority.
	edge_list = [] # (iot, ap, edge_priority(iot,ap))
	for device in w.iots:
		edge_list += device.get_edge_weights(w.aps)
	edge_list.sort(key=lambda x: x[2], reverse=True) # Biggest edge_priority first.

	# Go through the list and associate by edge.
	num_iots_total = len(w.iots)
	num_iots_associated = 0
	for iot, ap, edge_priority in edge_list:
		if iot.is_associated() or num_iots_associated == num_iots_total: 
			continue
		else:
			if iot.do_associate(ap) == True:
				num_iots_associated += 1

	return num_iots_associated == num_iots_total





