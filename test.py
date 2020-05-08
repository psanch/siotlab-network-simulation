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

# objects.py
max_capacity = 1000	# Determine the capacity for APs.

min_demand = 0		# Determine the demand range for IOTs.
max_demand = 100

# score.py
number_of_aps = 7 	# Currently must <= 7 (for visuals) due to color implementation.
number_of_iots = 50 
verbose = False 	# Will block on input (Window.plot), any key will continue. Not good for batch tests.
print(Score.approaches) # See implemented strategies here.

# === Testing Area === 

s = Score('greedy_rssi', 1)
print(s)
s = Score('round_robin', 10)
print(s)




