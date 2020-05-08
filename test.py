from objects import *
from simulate import *
from strategies import *

associate_strategy = greedy_rssi
"""
round_robin
greedy_rssi
"""

def test():
	w = Window(gen_iots = 70, gen_aps = 6)

	if associate_strategy(w) == False:
		print("Association Failed!")
		return False

	w.plot()

test()
