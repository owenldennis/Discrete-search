# -*- coding: utf-8 -*-
"""
Created on Tue Dec 22 06:54:22 2020

@author: owen
"""


class Hill_climber():
    """
        Class Hill climber is an abstracted hill climbing algorithm.
        Requires the current state and two methods:
            - states_generator must be an iterator over all of the next possible states for any given state
            - target_func must evaluate any given state (higher is better)
    
    """
    

    def __init__(self,target_func,state,states_generator,verbose=False):
        self.target_func=target_func
        self.state=state
        self.states_generator=states_generator
        self.verbose=verbose
            
    def climb(self):
        """
        

        Parameters
        ----------
        None

        Returns
        -------
        next_state : TYPE matches the type of the self.state parameter, or None if no better state found
            DESCRIPTION. the next state after the best move (None if no improving move available)
        best : TYPE float/integer (matches the output of self.target_func)
            DESCRIPTION. evaluation of the best state found in this step

        """
        
        best=self.target_func(self.state)
        next_state=None
        for state in self.states_generator(self.state):
                score=self.target_func(state)
                if score>best:
                    next_state=state
                    best=score
        
        return next_state,best
    
    def climb_to_summit(self):
        """
        

        Returns
        -------
        TYPE same as self.state
            DESCRIPTION. the state corresponding to a local maximum found by repeated climb() steps
        summit_score : TYPE float/integer (output of self.target_func)
            DESCRIPTION.the score for the local maximum found

        """
        at_summit=False
        while not at_summit:
            next_state,summit_score=self.climb()
            if next_state:
                self.state=next_state                    
            else:
                at_summit=True
        
        return self.state,summit_score
                    

class Hill_climber_with_reset(Hill_climber):

    def __init__(self,target_func,state,states_generator,verbose=False):
        
        Hill_climber.__init__(target_func,state,states_generator,verbose)

                                          