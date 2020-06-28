"""Implements the Node, AP and IOT classes."""

from random import randint
import numpy as np
import matplotlib.pyplot as plt
import math 

COLORS = ['b','g','r','c','m','y','k','w']

         
class Node:
    """Used by children to store position on a cartesian coordinate plane."""

    def __init__(self, x=0, y=0):
        """Instantiate a node object with 2-d coordinates."""
        self.x = x
        self.y = y

    def get_dist(self, other: 'Node') -> float:
        # Returns the euclidean distance between two nodes
        return ((other.x - self.x) ** 2 + (other.y - self.y) ** 2) ** 0.5

class AP(Node):
    """Model (remaining) capacity based on iot nodes that are associated with it."""

    ssid = 0
    max_capacity = 1000
    RANGE = 1250

    def __init__(self, x=0, y=0, used_capacity=0):
        """Create an AP Object with max_capacity."""

        super().__init__(x,y)

        self.max_capacity = AP.max_capacity
        self.used_capacity = used_capacity
        self.iots = []

        self.ssid = AP.ssid
        AP.ssid += 1

        self.color = COLORS[self.ssid % len(COLORS)]

    def __str__(self):
        return f"AP[{self.ssid}]"

    def __repr__(self):
        return f"AP[{self.ssid}]"

    def get_remaining_capacity(self) -> int:
        """Returns the remaining capacity of the AP."""

        return self.max_capacity - self.used_capacity

    def get_load_factor(self) -> float:
        """Returns the load factor of the AP."""

        return self.used_capacity / self.max_capacity

    def disconnect(self) -> float:
        """Disconnects AP from all nodes, for both links."""

        for iot in self.iots:
            iot.ap = None
            iot.color = 'w'

        self.iots = []

        self.used_capacity = 0

    def print_stats(self):
        """Prints both remaining capacity and load factor of the AP."""

        print(f"Remaining capacity:\t{self.get_remaining_capacity()}")
        print(f"Load Factor:\t{self.get_load_factor()}")

class IOT(Node):
    """Model resource demands and AP association."""
    min_demand = 0
    max_demand = 100
    P_Tx = 100 # mWatt
    GAMMA = 2.2
    R_0 = 1 #mW
    PL_0 = -27.5
    ssid = 0

    def __init__(self, x=0, y=0, demand=randint(min_demand,max_demand), ap=None):
        """ Create IOT object with resource demand and (optional) an ap to be associated to."""

        super().__init__(x,y)

        self.demand = demand
        self.ap = ap

        self.ssid = IOT.ssid
        IOT.ssid += 1

        self.color = 'w'

    def __str__(self):
        return f"IOT[{self.ssid}]"

    def __repr__(self):
        return f"IOT[{self.ssid}]"

    def is_associated(self):
        """Return a boolean indiciating if self is associated based on self.ap."""

        return self.ap != None # None = False, else = True

    def do_evaluate(self, ap) -> bool:
        """Considers the validity of ap as a candidate for association.

        Return:
        bool:    If true, ap is a valid candidate for association.
        """
        if (ap.used_capacity + self.demand) / ap.max_capacity <= 1:
            return True
        else:
            return False

    def do_associate(self, ap) -> bool:
        """Try to associate self with ap. Updates ap capacity if successful. Returns status.

        Keyword Arguments:
        ap:        AP to be associated with.

        Return:
        bool:    Returns true and updates ap.used_capacity if association was successful.
                No side effects upon False.

        """

        if self.do_evaluate(ap) == False:
            return False
        else:
            self.ap = ap # Create double-sided links
            ap.iots.append(self)

            ap.used_capacity += self.demand # Update ap capacity and iot color
            self.color = ap.color
            return True

    def edge_priority_function(self, ap):
        """Return the custom cost between self and ap."""
        d = self.get_dist(ap)
        if d == 0:
            d = 1
        else:
            d = 1 / d
        return d * ap.get_remaining_capacity()

    def get_edge_weights(self, aps):
        """Return a list of tuples (self, ap, priority) based on consiering the aps from the iot."""

        return [(self, ap, self.edge_priority_function(ap)) for ap in aps]


    def get_candidate_aps(self, aps):
        """Return a list of valid aps. Filter defined in do_evaluate."""

        return [ap for ap in aps if self.do_evaluate(ap) == True]

    def get_rssi_to_aps(self, aps):
        """Returns a list of (rssi, ap) from the iot node."""

        l = []
        for ap in aps:
            tmp = self.get_dist(ap) ** 2
            if tmp == 0:
                tmp = 1
            else:
                tmp = 1/tmp
            l.append((tmp, ap))
        return l

    def calc_power_loss(self, ap):
 
        dist = self.get_dist(ap) #Rji distji   
        #if dist > ap.RANGE: return 0.0
        pl = IOT.PL_0 + 10*IOT.GAMMA*math.log10(dist/IOT.R_0) #+ X 
        p_r = IOT.P_Tx - pl
        return p_r
        
    def print_stats(self):
        print(f"Demand:\t{self.demand}")

    def rand_demand():
        """Return a random demand value within the class constraints."""

        return randint(IOT.min_demand, IOT.max_demand)
