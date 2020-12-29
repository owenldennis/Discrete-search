# -*- coding: utf-8 -*-
"""
Created on Mon Dec 21 11:52:45 2020

@author: owen
"""

import numpy as np


class Queen():

    def __init__(self, row, column):
        self.row = row
        self.column = column
    
    def set_score(self,score):
        self.score=score


    def print_info(self):
        print("Row {0}, Column {1}".format(self.row, self.column))
        
        
        
class NQueens_state():
    
    def __init__(self,rows,columns):
        self.row_list = np.random.choice(range(rows),size=columns)
        self.queen_list = [Queen(self.row_list[i], i) for i in range(columns)]
        self.rows=rows
        self.columns=columns
    
    def get_state_as_coords(self,queen_list=None):
        if not queen_list:
            queen_list=self.queen_list
        
        return [(queen.row,queen.column) for queen in queen_list]
    
    def convert_coords_to_queen_list(self,coords_list):
        return [Queen(coords[0],coords[1]) for coords in coords_list]
    
    
    def one_step_iterator(self,queen_list):
        if not queen_list:
            queen_list=self.queen_list
        
        for queen in queen_list:
            current_row=queen.row
            for i in range(self.rows):
                queen.row=i
                yield queen_list
            queen.row=current_row

        
    def is_attacking(self,q1,q2):
        """
        
    
        Parameters
        ----------
        q1 : TYPE queen
            DESCRIPTION.
        q2 : TYPE queen
            DESCRIPTION.
    
        Returns 
        -------
        int 1 if queens are attacking each other, 0 if not
            DESCRIPTION.
    
        """
        # if the queens are the same object they are not attacking each other
        if q1==q2:
            return 0
        # if the queens are on the same row they are attacking
        if q1.row==q2.row:
            return 1   
        # if the queens are on a diagonal they are attacking
        row_diff = abs(q2.row-q1.row)
        col_diff = abs(q2.column-q1.column)
        if row_diff == col_diff:
            return 1
        # otherwise they are not attacking
        return 0
    
    
    def evaluate_position(self,nqueens_state=None):
        """
        

        Parameters
        ----------
        nqueens_state : TYPE NQueens_state object
            DESCRIPTION. state to be evaluated.  If not passed, current object is evaluated

        Returns integer
        -------
        TYPE 
            DESCRIPTION. total of all interactions between queens in nqueens_state

        """
        return sum([self.is_attacking(queen1,queen2) for queen1 in nqueens_state.queen_list
                    for queen2 in nqueens_state.queen_list])
            
    
        
        
        
        







def check_interaction(q1, q2):
    if q1==q2:
        return 0
    if q1.row==q2.row:
        return 1
    row_diff = abs(q2.row-q1.row)
    col_diff = abs(q2.column-q1.column)
    if row_diff == col_diff:
        return 1
    return 0

class Move():
    
    def __init__(self,queen,row):
        self.queen=queen
        self.row=row

    





class Hill_climber_8queens():

    def __init__(self,rows=8,columns=8,verbose=False):


        row_list=np.random.choice(range(rows),size=columns)
        
        self.rows=rows
        self.columns=columns
        self.queens = [Queen(row_list[i], i) for i in range(columns)]
        self.verbose=verbose
        if self.verbose:
            [q.print_info() for q in self.queens]


    def count_interactions(self):
        return sum([check_interaction(q1,q2) for q1 in self.queens for q2 in self.queens])
                    
            
    def climb(self, reset=False):
        ### iterate through all moves and find the best one
        
        best=self.count_interactions()
        move=None
        for queen in self.queens:
            current_row = queen.row
            for row in range(self.rows):
                queen.row=row
                score=self.count_interactions()
                if score<best:
                    move=Move(queen,row)
                    best=score
            queen.row=current_row
        
        return move,best
        
            
                
        
        



if __name__ == '__main__':
    h = Hill_climber_8queens()

    h.climb()
