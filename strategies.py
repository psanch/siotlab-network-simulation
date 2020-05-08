
def round_robin(w) -> bool:
	m = len(w.aps)
	i = 0

	for device in w.iots:
		if device.do_associate(w.aps[i%m]) == False:
			return False
		i += 1
	return True

def greedy_rssi(w) -> bool:

	for device in w.iots:
		# Process the aps for validity and sort them by RSSI (bigger is better)
		valid_aps = device.get_candidate_aps(w.aps)
		distances = device.get_rssi_to_aps(valid_aps)
		distances.sort(reverse=True, key = lambda x: x[0])

		print(distances)

		i = 0
		num_aps = len(w.aps)
		while i < num_aps:
			if (device.do_associate(distances[i][1])) == True:
				print(f"Associated IOT[{device.ssid}] with {w.aps[i]}.")
				device.print_stats()
				w.aps[i].print_stats()
				break
			else:
				i+=1
		else:
			return False
	return True



