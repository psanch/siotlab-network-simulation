"""Implements the Score class. Allows the scoring of different approaches on a given Window."""

from objects import *
from simulate import *
from strategies import *
from collections import defaultdict

class Result:
    """Implements a class that holds the results for one instance of the experiment."""

    def __init__(self, name, valid, scores: list):
        self.name = name
        self.scores = scores    # each index will hold a different type of score from Score.scoring_methods
        self.valid = valid

    def __add__(self, other):
        """Defines addition '+' between two Result objects."""

        l = []
        for i in range(len(self.scores)):
            l.append(self.scores[i] + other.scores[i])
        return Result(self.name, self.valid and other.valid, l)

    def __iadd__(self, other):
        """Defines incremental addition '+=' between two Result objects."""

        self = self + other
        return self

    def __truediv__(self, other: int):
        """Defines true division '/' between a Result and Int object."""

        return Result(self.name, self.valid, [score/other for score in self.scores])

    def __itruediv__(self, other: int):
        """Defines incremental true division '/=' between a Result and an Int object."""

        self = self / other
        return self

    def __repr__(self):
        return f"Result({self.name}, {self.valid}, {self.scores})"

    def __str__(self):
        return f"Result({self.name}, {self.valid}, {self.scores})"

    def isValid(self) -> bool:
        """Determines whether or not this score is valid (not a failed attempt)."""

        return self.valid

class Score:
    """Implement a class that will run n experiments and return a comprehensive score.

    Object parameters controlled by class variables at object creation time.
    """

    number_of_trials = 10 # Guarantees this number of trials will be ran for all approaches. 
    verbose = False # Not good for batch tests.
    plot = False# Plot will block on input, any key will continue.

    approaches = { # Add strategies here. This dict should be comprehensive.
        'greedy_rssi': greedy_rssi,
        'round_robin': round_robin,
        'greedy_demand_weighted_rssi': greedy_demand_weighted_rssi,
        'greedy_edge_based': greedy_edge_based,
        'greedy_resorted_edge_based': greedy_resorted_edge_based,
    }

    approaches_ordered = approaches.keys() # Don't touch; used for consistent key ordering

    scoring_methods = {
        'get_sum_rssi': Window.get_sum_rssi,
        'get_sum_remaining_capacity': Window.get_sum_remaining_capacity,
        'get_demand_weighted_sum_rssi': Window.get_demand_weighted_sum_rssi
    }
    scoring_methods_ordered = scoring_methods.keys() # Don't touch; used for consistent key ordering

    def __init__(self):
        """Initialize a Score object that runs n experiments."""

        counter_scores = {}
        self.results = []
        self.cumulative = []
        self.w = None 

        approaches = Score.approaches_ordered
        for approach in approaches: # Make a dummy scoring variable for compound addition
            counter_scores[approach] = Result(approach, True, len(Score.scoring_methods_ordered) * [0.0])

        temp = {}    # Dictionary will be used to store scores for a given window for all approaches

        successful_attempts = 0
        total_attempts = 0

        while successful_attempts < Score.number_of_trials: # Guarantee n Windows where all approaches succeed
            total_attempts += 1
            w = Window()
            self.w = w 
            fail_flag = False
            for approach in approaches: # Test every approach on w
                temp[approach] = self.experiment(w, approach=approach)
                if temp[approach].isValid() == False: # If any approach fails, break
                    if Score.verbose:
                        print(f"{approach} failed.")
                    fail_flag = True
                    break
                w.cleanup()

            if fail_flag == False: # Only consider the results if all approaches succeed
                for approach in approaches:
                    counter_scores[approach] += temp[approach] # Add each approach's result to cumulative
                successful_attempts += 1
                self.results.append([[data for data in temp[approach].scores] for approach in approaches])


        self.cumulative.append(Result("Labels", False, [method for method in Score.scoring_methods_ordered]))

        for approach in approaches: # Average over number of trials
            counter_scores[approach] /= successful_attempts
            self.cumulative.append(counter_scores[approach])

    def experiment(self, w: Window, approach: str='round_robin') -> Result:
        """Run one instance of a specified test and return Result object.

        Keyword Arguments:
        w:        The Window to associate with approach
        verbose:        True for real-time updates.
        approach:    Pick the strategy for association to be used.

        Return:
        Result object with valid scores for all methods in Score.scoring_methods_ordered.
        """

        scores = []

        if Score.approaches[approach](w) == False: # Attempt approach on w
            if Score.verbose == True:
                print("Association Failed!")
            return Result(approach, False, len(Score.scoring_methods_ordered) * [-1])
        else:
            # Creates a Result with valid scores for all methods in Score.scoring_methods_ordered.
            for score_function_name in Score.scoring_methods_ordered:
                scores.append(Score.scoring_methods[score_function_name](w))

        if Score.plot == True:
            w.plot()

        return Result(approach, True, scores)
