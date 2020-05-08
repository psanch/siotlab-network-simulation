"""Interface for the IOT-AP association experiment."""

from objects import *
from simulate import *
from strategies import *
from score import *

# The import statements (and code structure in general) isn't great for performance
# but it will (hopefully) get us readability when modifying code. Here's a quick tutorial
# on how to tweak the parameters of the simulation. 

# Parameter modification can be accessed through this file. They are stored in class
# variables which are preserved in object variables upon construction. In other words,
# an object is effectively immutable once it has been created. It would be trivial to
# go back and add the option to save all results, but I am only saving the relevant stats
# for the purposes of preserving memory. 

# simulate.py
Bounds.x_max = 100	# Determine the size of the area in which Nodes will exist. 
Bounds.x_min = -100
Bounds.y_max = 100
Bounds.y_min = -100

Window.number_of_aps = 7 	# Currently must <= 7 (for visuals) due to color implementation.
Window.number_of_iots = 50 

# objects.py
AP.max_capacity = 1000	# Determine the capacity for APs.

IOT.min_demand = 0		# Determine the demand range for IOTs.
IOT.max_demand = 100

# score.py
Score.number_of_trials = 10 # Controls the number of trials ran for each approach.
Score.verbose = False # Plot will block on input, any key will continue. Not good for batch tests.
Score.approaches = { # Add strategies here. This should be comprehensive.
	'greedy_rssi': greedy_rssi,
	'round_robin': round_robin,
	'greedy_demand_weighted_rssi' : greedy_demand_weighted_rssi
}

Score.scoring_methods = {
	'get_sum_rssi': Window.get_sum_rssi,
	'get_sum_remaining_capacity': Window.get_sum_remaining_capacity,
	'get_demand_weighted_sum_rssi': Window.get_demand_weighted_sum_rssi
}
Score.scoring_methods_ordered = Score.scoring_methods.keys() # Don't touch. For consistent ordering.

# === Testing Area === 

s = Score() 
print(s.results)


