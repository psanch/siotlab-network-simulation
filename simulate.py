from random import randint
from objects import *

class Bounds:
	"""Container to hold 2-d cartesian coordinates."""

	def __init__(self, x_min: int=-100, x_max: int=100, y_min: int=-100, y_max: int=100):
		""" Create a Bounds object based on x/y min/max.

		x_max:		Maximum value for x-coordinates.
		x_min:		Minimum value for x-coordinates.
		y_max:		Maximum value for x-coordinates.
		y_min:		Minimum value for x-coordinates.
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

	def __init__(self, gen_iots: int=100, gen_aps: int=8, iots: [IOT]=[], aps: [AP]=[], bounds = Bounds()):
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

	def plot(self):
		fig = plt.figure()

		for i in self.iots:
			plt.plot(i.x, i.y, i.color + 'o')

		for a in self.aps:
			plt.plot(a.x, a.y, a.color + '*')

		fig.show()
		input()

