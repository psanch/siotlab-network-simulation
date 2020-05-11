# siotlab-network-simulation
## Simulation tool written in Python to test the efficacy of various approaches when trying to associate IoTs to APs.

### Files:

#### objects.py
Implements the Node, AP and IOT classes. AP and IOT inherit from Node for positional behavior. IOTs can associate to APs, and this is done by keeping links from both directions. When an IOT associates to an AP, that AP's usage is incremented by the demand presented by the IOT.

#### simulate.py
Implements the Bounds and Window classes. Location and simulation infrastructure for the experiment. Window is the simulation state-- we are considering IOT association in a window of time for a given context. Window also has methods to populate the state with IOTs or APs. Furthermore, it can also generate state-wide scoring metrics. These are aggregated by the Score class.

#### score.py
Implements the Score class. Instantiation of a Score object will conduct an experiment with parameters specified by class variables in the respective modules. The Score class allows the user to conduct N trials for all approaches for a given context, and averages the scores over the entire set.

#### test.py
Interface for the IOT-AP association experiment. Find all the parameters aggregated here in their class variables. Instantiations of the Score object are equivalent to executing the experiment with the defined parameters.

#### strategies.py
Implements various strategies for associating IOTs to APs. Please implement yours here. We are looking for the best method to associate IOT devices to APs. We want to optimize with respect to the metrics in the Score class, although we may consider more.

I recommend you start by looking at test.py, as it is the interface for the tool.  
