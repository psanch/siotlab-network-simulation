# -*- coding: utf-8 -*-
"""
Created on Tue Jun 23 16:03:21 2020

@author: ranofal
"""
import time, array, random, copy, math
import numpy as np
import deap 
from deap import algorithms, base, benchmarks, tools, creator

from wsn import WSN
from simulate import Window, Bounds
from objects import IOT, AP


def cxTwoPointCopy(ind1, ind2):

    """Execute a two points crossover with copy on the input individuals. The

    copy is required because the slicing in numpy returns a view of the data,

    which leads to a self overwritting in the swap operation. It prevents

    ::
        >>> import numpy

        >>> a = numpy.array((1,2,3,4))

        >>> b = numpy.array((5,6,7,8))

        >>> a[1:3], b[1:3] = b[1:3], a[1:3]

        >>> print(a)

        [1 6 7 4]

        >>> print(b)

        [5 6 7 8]

    """
    size = len(ind1)
    cxpoint1 = random.randint(1, size)
    cxpoint2 = random.randint(1, size - 1)
    if cxpoint2 >= cxpoint1:
        cxpoint2 += 1
    else: # Swap the two cx points
        cxpoint1, cxpoint2 = cxpoint2, cxpoint1
        
    ind1[cxpoint1:cxpoint2], ind2[cxpoint1:cxpoint2] = \
        ind2[cxpoint1:cxpoint2].copy(), ind1[cxpoint1:cxpoint2].copy()
    return ind1, ind2


def create_c_mat(m,n):
    c = np.zeros((m, n), dtype=int)
    c = (np.random.randint(0, m, size=n) == np.arange(m).reshape(-1, 1)).astype(int)
    return c 

def evaluate(individual):
    wsn = WSN.getInstance() 
    RT  = wsn.get_rates()
    C  = individual[0] 
    f1 = sum(sum(RT*C))
    f2 = len(np.where(~C.any(axis=1)))
    # a = []
    # for j, row in enumerate(C):
    #     if not all( v == 0 for v in row):
    #         a.append(1)
    #     else:
    #         a.append(0)
    # f1 = 0
    # f2 = 0
    # for j, row in enumerate(RT):
    #     f1+=sum([math.log10(1 + x * y) for x, y in zip(RT[j], C[j])])
    
    # for j, val in enumerate(a):
    #     f2+=val
    return f1, f2
    
def feasible(individual):
    # individual contains c [mxn] where m is number of aps n is numer of devices.
    
    wsn = WSN.getInstance() 
    RT  = wsn.get_rates()
    C = individual[0]
    cons_1 = 0 # 5c
    cons_2 = 0 # 5d
    cons_3 = 0 # 5e
    cons_4 = 0 # 5f

    for j, val in enumerate(C):
        cons_1 += val
    
    # 5d on the paper is between a pair of AP and IoT device only. However, we are looking at the entire system as an individual?
    for j, row in enumerate():
        cons_2+=sum([math.log10(1 + x * y) for x, y in zip(RT[j], C[j])])

    #for j, row in enumerate(c):
    #    cons_3+=sum([x * y for x, y in zip(rssi[j], C[j])])

    # code for cons_4

    # ----------
    p_0 = 10 
    if cons_1 <= 1 and cons_2 >= p_0: # and cons_3 >= R_0 and cons_4 <= 1:
        return True
    else:
        return False
    
    
    
    
Bounds.x_max = 100	# Determine the size of the area in which Nodes will exist.
Bounds.x_min = -100
Bounds.y_max = 100
Bounds.y_min = -100

Window.number_of_aps = 3 	# Currently must <= 7 (for visuals) due to color implementation.
Window.number_of_iots = 5

# objects.py
AP.max_capacity = 1000	# Determine the capacity for APs.

IOT.min_demand = 0		# Determine the demand range for IOTs.
IOT.max_demand = 100


random.seed(100)
w = Window()
wsn = WSN()
iot_list = w.iots
ap_list = w.aps
wsn.calc_PL(ap_list,iot_list)
wsn.calc_SNR()
wsn.calc_rate()
print(wsn.get_rates())


#DEAP starts here
##############################################################################

creator.create("FitnessMulti", base.Fitness, weights=(1.0,-1.0))
creator.create("Individual", np.ndarray, fitness=creator.FitnessMulti)

toolbox = base.Toolbox()

toolbox.register("attr_bool", random.randint, 0, 1)
toolbox.register("individual", tools.initRepeat, creator.Individual, toolbox.attr_bool, n=100)
toolbox.register("population", tools.initRepeat, list toolbox.individual)


