from random import randint
import numpy as np
import matplotlib.pyplot as plt

COLORS = ['b','g','r','c','m','y','k','w']

class Node:
	"""Store position on a cartesian coordinate plane."""
	
	def __init__(self, x=0, y=0):
		self.x = x
		self.y = y

	def get_dist(self, other: 'Node') -> float:
		# Returns the euclidean distance between two nodes
		return ((other.x - self.x) ** 2 + (other.y - self.y) ** 2) ** 0.5

class AP(Node):
	"""Model (remaining) capacity based on iot nodes that are associated with it."""
	
	ssid = 0

	def __init__(self, x=0, y=0, used_capacity=0, max_capacity=1000):
		"""Create AP Object with max_capacity."""
		super().__init__(x,y)
		
		self.max_capacity = max_capacity
		self.used_capacity = used_capacity
		self.iots = []

		self.ssid = AP.ssid
		AP.ssid += 1

		self.color = COLORS[self.ssid]

class IOT(Node):
	"""Model resource demands and AP association."""
	
	min_demand = 0
	max_demand = 100

	ssid = 0
	
	def __init__(self, x=0, y=0, demand=0, ap=None):
		""" Create IOT object with resource demand and (optional) an ap to be associated to."""

		super().__init__(x,y)

		self.demand = demand
		self.ap = ap

		self.ssid = IOT.ssid
		IOT.ssid += 1

		self.color = 'w'

		if ap != None:
			assert(self.do_associate(ap) == True)

	def do_evaluate(self, ap) -> float:
		"""Considers the effect of self on ap.

		Return:
		float:	Returns the load factor of ap based on used/max capacity.
		"""

		return (ap.used_capacity + self.demand) / ap.max_capacity

	def do_associate(self, ap) -> bool:
		"""Try to associate self with ap. Updates ap capacity if successful. Returns status.

		Keyword Arguments:
		ap:		AP to be associated with.

		Return:
		bool:	Returns true and updates ap.used_capacity if association was successful. 
				No side effects upon False.

		"""

		if self.do_evaluate(ap) > 1:
			return False
		else:
			self.ap = ap
			ap.iots.append(self)
			ap.used_capacity += self.demand
			self.color = ap.color
			return True

	def rand_demand():
		"""Return a random demand value within the class constraints."""

		return randint(IOT.min_demand, IOT.max_demand)