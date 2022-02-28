import numpy as np 
import random 

from src.utils import calculate_board_dim

def initialize(board, num_boards=5000, black_cell_factor=1.5):
    """
        initializes 5000 random board configurations as the first generation
    """
    # calculate the numbered cells
    numbered_cells = np.count_nonzero(board)
    
    # initialize black cells as 1.5x numbered_cells
    black_cells = round(black_cell_factor * numbered_cells)
    
    # calculate dimensions of board 
    height, width = calculate_board_dim(board)

    # convert numbered cell indices to 1D indices 
    numbered_cell_indices = np.nonzero(board)
    numbered_cell_1d_indices = []
    for i in range(numbered_cells):
        numbered_cell_1d_indices.append(int (numbered_cell_indices[0][i] * width + numbered_cell_indices[1][i]))
    
    # create 5000 boards, each with black_cells number of black cells
    random_boards = np.zeros((5000, height, width), np.int32)
    for k in range(num_boards):
        random_boards[k] = board
        # remove indices of numbered cells as black cells can't be numbered 
        choices = [index for index in range(height * width) if index not in numbered_cell_1d_indices]
        # choose 1d indices for random sampling 
        black_cell_1d_indices = random.sample(choices, black_cells)
        black_cell_1d_indices = np.asarray(black_cell_1d_indices)
        # convert 1d to 2d indices
        black_cell_indices = (black_cell_1d_indices / width).astype(int), black_cell_1d_indices % width
        
        # set black cells as -1 
        for i in range(black_cells):
            random_boards[k, black_cell_indices[0][i], black_cell_indices[1][i]] = -1

    return random_boards