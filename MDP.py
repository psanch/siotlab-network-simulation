# -*- coding: utf-8 -*-
"""
Implement MDP 
"""
Actions = ['pick','associate'] #there are 2 actions only for now

class State:
    """Implements a class that represents a state in MDP."""
    def __init__(self, s):
        """
        
        Parameters
        ----------
        s : TYPE
            id a number

        Returns
        -------
        None.

        """
        self.id = s
        self.
        
    def reward(self, a, state):
        """
        What is the reward from this state taking action 

        Parameters
        ----------
        a : Action 
            DESCRIPTION.
        state : State
            the next state

        Returns
        -------
        None.

        """
        