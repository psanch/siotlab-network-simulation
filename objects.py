from random import randint

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
	
	def __init__(self, x=0, y=0, used_capacity=0, max_capacity=1000, associates=[]):
		super().__init__(x,y)
		
		self.max_capacity = max_capacity
		self.used_capacity = used_capacity
		self.associates = associates

class IOT(Node):
	"""Model resource demands and AP association."""
	
	min_demand = 0
	max_demand = 100
	
	def __init__(self, x=0, y=0, demand=0, ap=None):
		""" Create IOT object with resource demand and (optional) an ap to be associated to."""

		super().__init__(x,y)

		self.demand = demand
		self.ap = ap

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
			ap.associates.append(self)
			ap.used_capacity += demand
			return True

	def rand_demand():
		"""Return a random demand value within the class constraints."""

		return randint(IOT.min_demand, IOT.max_demand)

class Bounds:
	"""Container to hold 2-d cartesian coordinates."""

	def __init__(self, x_min: int=-100, x_max: int=100, y_min: int=-100, y_max: int=100):
		""" Create a Bounds object based on x/y min/max.

		x_max:		Maximum value for x-coordinates.
		x_min:		Maximum value for x-coordinates.
		y_max:		Maximum value for x-coordinates.
		y_min:		Maximum value for x-coordinates.
		"""

		self.x_max = x_max
		self.x_min = x_min
		self.y_max = y_max
		self.y_min = y_min

	def rand_x(self):
		return randint(self.x_min, self.x_max)

	def rand_y(self):
		return randint(self.y_min, self.y_max)

class Window:

	def __init__(self, gen_iots: int=100, gen_aps: int=10, iots: [IOT]=[], aps: [AP]=[], bounds = Bounds()):
		""" Create a Window for IOT/AP association. May have to generate IOT/AP's.

		Keyword Arguments:
		gen_iots:	Number of IOT objects to be generated.
		gen_aps:	Number of AP objects to be generated.
		iots:		List of pre-defined IOT objects.
		aps:		List of pre-defined AP objects.
		bounds:		Boundaries to constrain object generation if necessary.
		"""

		self.iots = iots + [self.do_generate_iot(bounds) for _ in range(gen_iots)]
		self.aps = aps + [self.do_generate_ap(bounds) for _ in range(gen_aps)]

	def do_generate_iot(self, bounds: Bounds):
		"""Instanciate an IOT based on constraints in bounds object (x,y) and IOT class (demand)."""

		return IOT(x=bounds.rand_x(), y=bounds.rand_y(), demand=IOT.rand_demand())

	def do_generate_ap(self, bounds: Bounds):
		"""Instanciate an AP based on constraints in bounds object (x,y)."""

		return AP(x=bounds.rand_x(), y=bounds.rand_y())



