import numpy as np 
import random 

from src.utils import calculate_adjacent_black_cells, calculate_absolute_differences

def calculate_fitness(board):
    """
        calculates fitness value of board 
        f1 = number of adjacent black cells
        f2 = sum of absolute differences between white cells visible from numbered cells and actual number on cells
    """
    # calculate f1 
    f1 = calculate_adjacent_black_cells(board)

    # calculate f2 
    f2 = calculate_absolute_differences(board)
    
    # return cumulative fitness of a board    
    return f1 + f2