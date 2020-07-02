from math import sin
from deap import base
from deap import tools

def evalFct(individual):
    """Evaluation function for the individual."""
    x = individual[0]
    return (x - 5)**2 * sin(x) * (x/3),

def feasible(individual):
    """Feasibility function for the individual. Returns True if feasible False
    otherwise."""
    if 3 < individual[0] < 7:
        return True
    return False

def distance(individual):
    """A distance function to the feasibility region."""
    return (individual[0] - 5.0)**2

toolbox = base.Toolbox()
toolbox.register("evaluate", evalFct)
toolbox.decorate("evaluate", tools.DeltaPenalty(feasible, 7.0, distance))
hof = tools.HallOfFame(1, similar=numpy.array_equal)
tats = tools.Statistics(lambda ind: ind.fitness.values)