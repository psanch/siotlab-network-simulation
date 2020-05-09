"""Implements the Bounds and Window classes. Location and simulation infrastructure for the experiment."""

from random import randint
from objects import *

class Bounds:
	"""Container to hold objects with 2-d cartesian coordinates."""

	x_max = 100
	x_min = -100
	y_max = 100
	y_min = -100

	def __init__(self):
		""" Create a Bounds object based on x/y min/max.

		x_max:		Maximum value for x-coordinates.
		x_min:		Minimum value for x-coordinates.
		y_max:		Maximum value for x-coordinates.
		y_min:		Minimum value for x-coordinates.
		"""

		self.x_max = Bounds.x_max
		self.x_min = Bounds.x_min
		self.y_max = Bounds.y_max
		self.y_min = Bounds.y_min

	def rand_x(self):
		return randint(self.x_min, self.x_max)

	def rand_y(self):
		return randint(self.y_min, self.y_max)

class Window:
	"""Container to hold a context in which we associate IOTs to APs."""

	number_of_aps = 7 # Currently must <= 7 (for visuals) due to color implementation.
	number_of_iots = 50

	def __init__(self, gen_iots: int='Window.number_of_iots', gen_aps: int='Window.number_of_aps', bounds = Bounds()):
		""" Create a Window for IOT/AP association. May have to generate IOT/AP's.

		Keyword Arguments:
		gen_iots:	Number of IOT objects to be generated.
		gen_aps:	Number of AP objects to be generated.
		iots:		List of pre-defined IOT objects.
		aps:		List of pre-defined AP objects.
		bounds:		Boundaries to constrain object generation if necessary.
		"""

		AP.ssid = 0
		IOT.ssid = 0
		self.iots = [self.do_generate_iot(bounds) for _ in range(Window.number_of_iots)]
		self.aps = [self.do_generate_ap(bounds) for _ in range(Window.number_of_aps)]

	def do_generate_iot(self, bounds: Bounds):
		"""Instanciate an IOT based on constraints in bounds object (x,y) and IOT class (demand)."""

		return IOT(x=bounds.rand_x(), y=bounds.rand_y(), demand=IOT.rand_demand())

	def do_generate_ap(self, bounds: Bounds):
		"""Instanciate an AP based on constraints in bounds object (x,y)."""

		return AP(x=bounds.rand_x(), y=bounds.rand_y())

	def get_sum_rssi(self) -> float:
		"""Return the sum of all RSSIs for all APs to their associated IOTs"""

		s = 0
		for device in self.iots:
			s += device.get_dist(device.ap)
		return s

	def get_demand_weighted_sum_rssi(self) -> float:
		"""Return the sum of all RSSIs for all APs to their associated IOTs"""

		s = 0
		for device in self.iots:
			s += (device.get_dist(device.ap) * device.demand)
		return s

	def get_sum_remaining_capacity(self) -> int:
		"""Return the sum of remaining capacity for all APs."""

		remaining = 0
		for ap in self.aps:
			remaining += ap.get_remaining_capacity()
		return remaining

	def plot(self):
		"""Plot the Window and assign colors to nodes.

		WARNING: BLOCKS!! Note the call to input().
		"""

		fig = plt.figure()

		for i in self.iots:
			plt.plot(i.x, i.y, i.color + 'o')

		for a in self.aps:
			plt.plot(a.x, a.y, a.color + '*')

		fig.show()
		input()
