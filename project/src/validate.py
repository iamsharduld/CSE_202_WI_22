import numpy as np 

from src.utils import calculate_board_dim, calculate_connected_components, calculate_adjacent_black_cells, calculate_visible_cells

def validate_board(board):
    """
        returns true if the input board is a valid solution to a kuromasu puzzle, false otherwise
    """
    # calculate board dimensions
    height, width = calculate_board_dim(board)
    

    # check that no 2 black cells are adjacent
    adjacent_black_cells = calculate_adjacent_black_cells(board)
    if adjacent_black_cells > 0:
        return False
    # print("Constraint 1 passed ")
    
    # check that all white cells are connected 
    connected_components = calculate_connected_components(board)
    if connected_components != 1:
        return False

    # print("Constraint 2 passed ")

    # check that the numbered cells are numbered correctly 
    numbered_cell_indices = np.argwhere(board > 0)
    for r, c in numbered_cell_indices:
        visible_cells = calculate_visible_cells(board, r, c)
        if visible_cells != board[r, c]:
            return False

    # print("Constraint 3 passed")    
    return True