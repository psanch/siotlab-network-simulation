# -*- coding: utf-8 -*-
"""
Created on Tue Jun 23 16:03:21 2020

@author: ranofal
"""
import time, array, random, copy, math, sys
import numpy as np 
from deap import algorithms, base, benchmarks, tools, creator
from scipy.spatial import ConvexHull
import sklearn.cluster as cluster
import matplotlib.pyplot as plt
from collections import defaultdict 
from wsn import WSN
from simulate import Window, Bounds
from objects import IOT, AP
from strategies import greedy_rssi, round_robin
import pdb 

class T:
    cnt = 0 

def create_c_mat_old(m,n):
    c = np.zeros((m, n), dtype=int)
    c = (np.random.randint(0, m, size=n) == np.arange(m).reshape(-1, 1)).astype(int) 
    return c
  
def create_c_mat(m,n):
    c = np.zeros((m, n), dtype=int)
    if random.random() < 0.2:
        #pick 20% of the rows and make them all zeros.
        c = (np.random.randint(0, m, size=n) == np.arange(m).reshape(-1, 1)).astype(int)
        for r in np.random.randint(0,m,int(m*.2)):
            c[r,] = 0 
    else:
        c = (np.random.randint(0, m, size=n) == np.arange(m).reshape(-1, 1)).astype(int)
    return c  

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
    #for now the we'll make the crossover by swtiching 2 columns
    size = len(ind1[0][0]) #find the length of the first row or 
    #size = ind1[0].shape(-1) #number of columns 
    #pdb.set_trace()
    cxcol1 = random.randint(0, size-1)
    cxcol2 = random.randint(0, size - 2)
    if cxcol2 >= cxcol1:
        cxcol2 += 1
    else: # Swap the two cx points
        cxcol1, cxcol2 = cxcol2, cxcol1
    
    ind1[0][:, [cxcol1,cxcol2]], ind2[0][:, [cxcol1,cxcol2]] =\
        ind2[0][:, [cxcol1,cxcol2]].copy(), ind1[0][:, [cxcol1,cxcol2]].copy()
        
    #ind1[cxpoint1:cxpoint2], ind2[cxpoint1:cxpoint2] = \
    #    ind2[cxpoint1:cxpoint2].copy(), ind1[cxpoint1:cxpoint2].copy()
    return ind1, ind2

def mutFlipAssociation_old(individual, indpb):
    C = individual[0]
    cols = C.shape[1] #find number of columns 
    if C.shape[0]==1: return individual,
    if random.random() < indpb:
        for i in range(cols):
            cur_col = C[:, i] 
            # There must be a 1 value in this column 
            one_loc = np.where(cur_col==1)[0][0] #the location of the 1 in the column
            zero_locs = np.where(cur_col==0)[0] #find zero locations 
            #pick a random zero loc from the zero_locs array
            zero_loc = zero_locs[random.randint(0, len(zero_locs)-1)]
            C[one_loc,i] = 0 #mutate the 1 to zero 
            C[zero_loc,i] = 1 #mutate this picked zero to 1
            #print('mutation occured')
    
    return individual,

def reassociate_by_col(C,r,i):
    cur_col = C[:, i]
    the_one = np.where(cur_col==1)[0]
    #if len(the_one)==0: continue # No ones in this column , simple ignore
    one_loc = np.where(cur_col==1)[0][0] #the location of the 1 in the column
    zero_locs = np.where(cur_col==0)[0] #find zero locations 
    zero_loc = zero_locs[random.randint(0, len(zero_locs)-1)]
    C[one_loc,i] = 0 #mutate the 1 to zero 
    C[zero_loc,i] = 1 #mutate this picked zero to 1


def mutFlipAssociation(individual, indpb):
    C = individual[0]
    cols = C.shape[1] #find number of columns 
    if C.shape[0]==1: return individual, #if there is only one AP in our system
    for i in range(cols):
        if random.random() < indpb:
            if random.random() < 0.75: # 75% of the time mutate for f1
                reassociate_by_col(C,0,i)
                # cur_col = C[:, i] 
                # the_one = np.where(cur_col==1)[0]
                # # There must be a 1 value in this column 
                # if len(the_one)==0: continue # No ones in this column , simple ignore
                # one_loc = np.where(cur_col==1)[0][0] #the location of the 1 in the column
                # zero_locs = np.where(cur_col==0)[0] #find zero locations 
                # #pick a random zero loc from the zero_locs array
                # zero_loc = zero_locs[random.randint(0, len(zero_locs)-1)]
                # C[one_loc,i] = 0 #mutate the 1 to zero 
                # C[zero_loc,i] = 1 #mutate this picked zero to 1
                # #print('mutation occured')
            else: #mutation for F2
                a_row = random.randint(0, C.shape[0]-1)
                for i,v in enumerate(C[a_row,:]):
                    if v==1: 
                      reassociate_by_col(C, a_row, i)
                
    return individual,

def get_func1(RT, C):
    f1 = math.log10(1 + sum(sum(RT*C)))
    return f1

def get_func2(C):
    f2 = C.shape[0] - len(np.where(~C.any(axis=1))[0])
    return f2

def run_greedy_rssi(w):
    for ap in w.aps:
        ap.disconnect()
    greedy_rssi(w)
    c = np.zeros((len(w.aps), len(w.iots)), dtype=int)
    for ap in w.aps:
        for d in ap.iots:
            c[ap.ssid][d.ssid]=1
    return c

def run_round_robin(w):
    for ap in w.aps:
        ap.disconnect()
    round_robin(w)
    c = np.zeros((len(w.aps), len(w.iots)), dtype=int)
    for ap in w.aps:
        for d in ap.iots:
            c[ap.ssid][d.ssid]=1
    return c

def evaluate_rate_nap(individual):
    wsn = WSN.getInstance() 
    RT  = wsn.get_rates()
    C  = individual[0] 
    f1 = math.log10(1 + sum(sum(RT*C))) 
    # f1 = sum(sum(RT*C))
    f2 = C.shape[0] - len(np.where(~C.any(axis=1))[0]) # Number of Rows that contains at least 1
    print("f1 = {}, f2 = {}".format(f1, f2))
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
    #print(f"f1={f1},f2={f2}")
    return f1, f2
    

#PROBABLY we need o cite this paper too
##Coelle Coello, C. A. Theoretical and numerical constraint-handling techniques used with 
##evolutionary algorithms: a survey of the state of the art. Computer Methods in Applied Mechanics 
##and Engineering 191, 1245–1287, 2002.

def feasible(ind):
    # ind contains c [mxn] where m is number of aps n is numer of devices.
    
    wsn = WSN.getInstance() 
    RT  = wsn.get_rates()
    Demands = wsn.Demands 
    C = ind[0]
    cons_4 = np.sum(C*wsn.Demands,axis=1)
        
    cons_1 = 0 # 5c
    cons_2 = 0 # 5d
    #cons_3 = 0 # 5e
    #cons_4 = 0 # 5f
    #pdb.set_trace()
    for j, val in enumerate(C):
        cons_1 += val
    
    # 5d on the paper is between a pair of AP and IoT device only. However, we are looking at the entire system as an individual?
    #THE calculation is wrong here, it sums twice 
    #for j, row in enumerate(RT):
    #    cons_2+=sum([x * y for x, y in zip(RT[j], C[j])])
    cons_2 = np.sum(wsn.PR*C,axis=0)
    cons_3 = np.sum(wsn.RSSI*C,axis=0)
    #for j, row in enumerate(c):
    #    cons_3+=sum([x * y for x, y in zip(rssi[j], C[j])])

    # code for cons_4

    # ----------
    p_0 = 10 
    R_0 = 0.00028284271247461896 #1/math.sqrt(2)*(half fo the boundary bound.min to bound.max)
    #if not cons_5_flag:
    #    #import pdb ; pdb.set_trace()
    #    print("max capacity have been reached %s"%T.cnt)
    #    T.cnt = T.cnt + 1
    cons_1_ones = np.ones(len(cons_1),int) #need to convert to an array
    cons_1_flag = all(cons_1_ones == 1) 
    cons_2_flag = all(cons_2 >= p_0)
    cons_3_flag = all(cons_3 >= R_0)
    cons_4_flag = all(cons_4 <= AP.max_capacity)
    
    if not cons_2_flag:
        print("cons_2 is not satisfied")
    if cons_1_flag and cons_2_flag and cons_3_flag and cons_4_flag: # and cons_3 >= R_0 and cons_4 <= 1:
        return True
    else:
        return False
    

def initial_AP_setting(k, iots, aps):
    """
    Using clustering alg to find the initial setting of AP
    :param k: number of clusters or number of AP's
    :return:
    """
    dL = []
    for i in iots:
        dL.append((i.x,i.y))
    cluster_object = cluster.KMeans(n_clusters=k, random_state=0).fit(dL)

    # center_list = random.sample(dL, k)
    # # Find all the clusters (that contain only one node) that are not in the center list
    # node_list = [p for p in dL if p not in center_list]
    # C_L = clustering.run_Lloyd_clustering(node_list, center_list, k, 'class')
    #self.C_L = C_L

    for i, ap in enumerate(cluster_object.cluster_centers_):
        x = int(round(ap[0]))
        y = int(round(ap[1]))
        if (x,y) in dL:  #in case the location of this ap lands on same locationof iot the move the ap a bit 
            x  += 3
            y  += 4
        aps[i].x, aps[i].y = x,y
    #print (dL) 
    
def main(N,M):
    
    Bounds.x_max = 2500    # Determine the size of the area in which Nodes will exist.
    Bounds.x_min = -2500
    Bounds.y_max = 2500
    Bounds.y_min = -2500
    bnd = Bounds()
    Window.number_of_aps = M    # Currently must <= 7 (for visuals) due to color implementation.
    Window.number_of_iots = N
    
    AP.max_capacity = 500    # Determine the capacity for APs.
    
    IOT.min_demand = 0        # Determine the demand range for IOTs.
    IOT.max_demand = 100
    
    random.seed(13)
    #import pdb ; pdb.set_trace()
    w = Window(bounds = bnd)
    wsn = WSN()
    # w.iots[0].x = -2500
    # w.iots[0].y = -2500
    # w.aps[0].x = 2500
    # w.aps[0].y = 2500 
    iot_list = w.iots
    ap_list = w.aps
    if M/N <= 0.1: #Only when the ration between APs/Devices is less than 10% (e.g: 100, 20)
        print("The ratio between #APs/#Device is less than 10 precent do clustering")
        initial_AP_setting(M, iot_list, ap_list)
    wsn.calc_rate(ap_list,iot_list)
    #print(wsn.get_rates())
    #import pdb; pdb.set_trace()
    rrC = run_round_robin(w)
    # RSSI startigy
    
    # #DEAP starts here
    # ##############################################################################
    
    creator.create("FitnessMulti", base.Fitness, weights=(1.0,-1.0))
    creator.create("Individual", np.ndarray, fitness=creator.FitnessMulti)
    
    toolbox = base.Toolbox()
    
    toolbox.register("attr", create_c_mat, M, N)
    toolbox.register("individual", tools.initRepeat, creator.Individual, toolbox.attr, n=1)
    
    toolbox.register("population", tools.initRepeat, list, toolbox.individual)
    
    toolbox.register("evaluate", evaluate_rate_nap)
    toolbox.register("mate", cxTwoPointCopy)
    toolbox.register("mutate", mutFlipAssociation, indpb=0.05)
    #toolbox.register("select", tools.selTournament, tournsize=3)
    toolbox.register("select", tools.selEpsilonLexicase, epsilon = 0.5) # selEpsilonLexicase epsilon = 0.5
    toolbox.decorate("evaluate", tools.DeltaPenalty(feasible,[-sys.maxsize -1 , sys.maxsize])) #[-sys.maxsize -1 , sys.maxsize])
    
    pop = toolbox.population(n=5000)
    
    hof = tools.HallOfFame(1, similar=np.array_equal)
   
    stats = tools.Statistics(lambda ind: ind.fitness.values)
    stats.register("avg", np.mean)
    stats.register("std", np.std)
    stats.register("min", np.min)
    stats.register("max", np.max)
    
    #algorithms.eaSimple(pop, toolbox, cxpb=0.75, mutpb=0.2, ngen=40, stats=stats,halloffame=hof)
    algorithms.eaMuCommaLambda(pop, toolbox, mu = 10, lambda_ = 50, cxpb=0.75, mutpb=0.2, ngen=120, stats=stats,halloffame=hof)

    return wsn, pop, stats, hof, w, iot_list, ap_list



def encircle(x, y, ax=None, **kw):
    if not ax: ax=plt.gca()
    p = np.c_[x,y]
    hull = ConvexHull(p)
    poly = plt.Polygon(p[hull.vertices,:], **kw)
    ax.add_patch(poly)

def plot_the_grid(approach, wsn, p, s, c_mat ,iots, aps):

    #c_mat = h[0][0]
    #print(c_mat)
    iot_coord_dict_x = defaultdict(list)
    iot_coord_dict_y = defaultdict(list)
    iot_coord_dict_ID = defaultdict(list)
    iot_coord_dict_size = defaultdict(list)
    fig1 = plt.figure()
    ax1 = fig1.add_subplot(111)
    colormap = plt.cm.gist_rainbow #nipy_spectral, Set1,Paired
    colors = [colormap(i) for i in np.linspace(0, 1, len(aps))]
    for ap_ssid, ap_row in enumerate(c_mat):
        if sum(ap_row)==0: 
            print(f"ap={ap_ssid} has no association")
            continue 
        iot_coord_dict_size[ap_ssid] = 85
        #[30 if d_i.message_type == 1 else 80 for d_i in ap.associated_devices]
        #iot_coord_dict_size
        iot_coord_dict_ID[ap_ssid] = [i for i, asso in enumerate(ap_row) if asso == 1]
        iot_coord_dict_x[ap_ssid] = [iots[i].x for i, asso in enumerate(ap_row) if asso == 1]
        iot_coord_dict_y[ap_ssid] = [iots[i].y for i, asso in enumerate(ap_row) if asso == 1]
        ax1.scatter(iot_coord_dict_x[ap_ssid], iot_coord_dict_y[ap_ssid], color = colors[ap_ssid], s = iot_coord_dict_size[ap_ssid])
        ax1.scatter(aps[ap_ssid].x, aps[ap_ssid].y, color = colors[ap_ssid], marker='^', s = 150)
        circle= plt.Circle((aps[ap_ssid].x, aps[ap_ssid].y), aps[ap_ssid].RANGE/2, color= colors[ap_ssid], fill=False)
        ax1.add_artist(circle)
        for j, txt in enumerate(iot_coord_dict_ID[ap_ssid]):
            ax1.annotate(txt, (iot_coord_dict_x[ap_ssid][j], iot_coord_dict_y[ap_ssid][j]))
        ax1.annotate("AP-{}".format(ap_ssid), (aps[ap_ssid].x, aps[ap_ssid].y))
        #encircle(iot_coord_dict_x[ap_ssid], iot_coord_dict_y[ap_ssid], ax1, ec = colors[ap_ssid], fc= colors[ap_ssid], alpha = 0.2)
    #for i in range(0,len(aps)):
    #    circle= plt.Circle((aps[i].x, aps[i].y), 20, color='g', fill=False)
    #    plt.gca().add_patch(circle)
    plt.title("{} - Number of IoT devices: {} - Number of APs: {}".format(approach, len(iots), len(aps)))
    #plt.show()
    fig1.savefig("{}_figure.svg".format(approach))
    

if __name__ == "__main__":
    #import pdb
    #pdb.set_trace()
    wsn, pop, stats, hof, wind, iot_list, ap_list = main(4,4) # 200, 35 does not plot
    print("DEAP succeeded")
    print("F1 for DEAP: {}. F2 for DEAP: {}.".format(get_func1(wsn.RT, hof[0][0]), get_func2(hof[0][0])))
    try:
        gC = run_greedy_rssi(wind)
        print("RSSI greedy succeeded")
        print("F1 for RSSI greedy: {}. F2 for RSSI greedy: {}.".format(get_func1(wsn.RT, gC), get_func2(gC)))
    except:
        print("RSSI greedy failed")
    try:
        rrC = run_round_robin(wind)
        print("RR succeeded")
        print("F1: for RR greedy: {}. F2: for RR greedy: {}.".format(get_func1(wsn.RT, rrC), get_func2(rrC)))
    except:
        print("RR greedy failed")
   
    plot_the_grid("DEAP eaMuCommaLambda", wsn, pop, stats, hof[0][0], iot_list, ap_list)
    plot_the_grid("RSSI Greedy", wsn, pop, stats, gC, iot_list, ap_list)
    plot_the_grid("RR Greedy", wsn, pop, stats, rrC, iot_list, ap_list)




