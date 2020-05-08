"""Implements the Score class. Allows the scoring of different approaches on a given Window."""

from objects import *
from simulate import *
from strategies import *

class Score:
	"""Implements a class that will run an experiment of n trials for a given strategy. Returns a comprehensive score."""

	number_of_aps = 7 # Currently must <= 7 (for visuals) due to color implementation.
	number_of_iots = 50 
	verbose = False # Plot will block on input, any key will continue. Not good for batch tests.
	approaches = { # Add strategies here.
		'greedy_rssi': greedy_rssi,
		'round_robin': round_robin
	}

	def __init__(self, approach: str, n: int=10):
		"""Create a Score object that runs n tests for a given association strategy.

		Side-effects:
		self.rssi:		Holds the sum of rssi value among associated pairs.
		self.waste:		Holds the sum of the remaining capacity for all APs.
		self.success_rate:	Holds the percentage of attempts that successfully 
					associated all IOTs to all APs.
		"""
		if Score.verbose == True:
			print(f"\nRunning {approach} {n} times...")

		self.approach = approach

		total_rssi = 0
		total_capacity = 0

		successful_attempts = 0
		total_attempts = 0
		
		while successful_attempts < n:
			total_attempts += 1

			# returns -1 if failure, else the score
			scores = self.one_test(verbose='Score.verbose', approach=Score.approaches[approach]) 

			if scores == (-1,-1): # Fail condition; try again
				continue

			rssi_score, capacity_score = scores

			total_rssi += rssi_score
			total_capacity += capacity_score

			successful_attempts += 1

		self.rssi = total_rssi
		self.waste = total_capacity
		self.success_rate = successful_attempts / total_attempts

		return None

	def __str__(self):
		return f"\nScore({self.approach}):\n\trssi:\t\t{self.rssi}\n\twaste:\t\t{self.waste}\n\tsuccess_rate:\t{self.success_rate}"

	def one_test(self, verbose='Score.verbose', approach=round_robin) -> int:
		"""Runs one instance of a specified test and return score.

		Keyword Arguments:
		verbose:		True for real-time updates.
		approach:	Pick the strategy for association to be used.

		Return:
		Score for the resulting association.
		"""

		# Set the parameters of the test.
		w = Window(gen_iots = Score.number_of_iots, gen_aps = Score.number_of_aps)

		if approach(w) == False:
			if verbose == True:
				print("Association Failed!")
			return (-1,-1)

		rssi_score = w.get_sum_rssi()
		capacity_score = w.get_sum_remaining_capacity()

		if verbose == True:
			w.plot()

		return rssi_score, capacity_score