from objects import *
from simulate import *
from strategies import *

associate_strategy = greedy_rssi
"""
round_robin
greedy_rssi
"""

def one_test(verbose=False, associate_strategy=round_robin) -> int:
	w = Window(gen_iots = 70, gen_aps = 5)

	if associate_strategy(w) == False:
		if verbose == True:
			print("Association Failed!")
		return -1

	score = w.get_sum_rssi()

	if verbose == True:
		print(f"SumRSSI: {score}")
		w.plot()

	return score

def n_tests(n=100, associate_strategy=round_robin):
	res = 0
	successful_tries = 0
	while successful_tries < n:
		attempt = one_test(verbose=False, associate_strategy=associate_strategy)
		if attempt >= 0:
			successful_tries += 1
			res += attempt
	return (res / n)

print(n_tests(associate_strategy = greedy_rssi))


