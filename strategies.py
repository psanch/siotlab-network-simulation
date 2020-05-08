class Approach:
	def __init__():
		pass

	def round_robin(self, w) -> bool:
		m = len(w.aps)
		i = 0

		for device in w.iots:
			if device.do_associate(w.aps[i%m]) == False:
				return False
			i += 1
		return True