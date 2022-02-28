import numpy as np
import random

from src.utils import calculate_board_dim

def crossover_left_right(board1, board2):
    """
        combines the left half of board1 with the right half of board2
    """
    # calculate dimensions of board 
    height, width = calculate_board_dim(board1)
    
    # initialize new board
    new_board = np.zeros((height, width))
    
    # extract left half of board1 and assign to left half of new board
    new_board[:, : int(width / 2)] = board1[:, : int(width / 2)]
    
    # extract right half of board2 and assign to right half of new board
    new_board[:, int(width / 2) :] = board2[:, int(width / 2) :]
    return new_board

def crossover_top_bottom(board1, board2):
    """
        combines the top half of board1 with the bottom half of board2
    """
    # calculate dimensions of board 
    height, width = calculate_board_dim(board1)
    
    # initialize new board
    new_board = np.zeros((height, width))
    
    # extract top half of board1 and assign to top half of new board
    new_board[: int(width / 2), :] = board1[: int(width / 2), :]
    
    # extract bottom half of board2 and assign to bottom half of new board
    new_board[int(width / 2) :, :] = board2[int(width / 2) :, :]
    return new_board

def crossover_odd_even(board1, board2):
    """
        combines the even rows of board1 with the odd rows of board2
    """
    # calculate dimensions of board 
    height, width = calculate_board_dim(board1)
    
    # initialize new board
    new_board = np.zeros((height, width))
    
    # extract even rows of board1 and assign to even rows of new board
    new_board[::2] = board1[::2]

    # extract odd rows of board2 and assign to odd rows of new board
    new_board[1::2] = board2[1::2]
    return new_board

def crossover(selected_boards, selection_ratio=0.25):
    """
        combines three types of crossover to create a new generation 
    """
    # Select selction_ratio boards from selection
    num_selected = selected_boards.shape[0]
    selected_indices = random.sample(range(num_selected), int(selection_ratio * num_selected))
    boards_from_selection = selected_boards[selected_indices]
    
    # Define number of boards for crossover
    num_boards_for_crossover = num_selected - boards_from_selection.shape[0]
    
    # Only use unselected boards for crossover
    unselected_indices = np.setdiff1d(range(num_selected), selected_indices)
    
    # Peform crossover
    boards_from_crossover = []
    for i in range(num_boards_for_crossover):
        # Select 2 random indices from unselected indices
        board_indices = np.random.choice(unselected_indices, 2, replace=False)

        # Perform left right crossover on one third of boards 
        if i%3 == 0:
            boards_from_crossover.append(crossover_left_right(selected_boards[board_indices[0]], selected_boards[board_indices[1]]))

        # Perform top bottom crossover on one third of boards 
        elif i%3 == 1:
            boards_from_crossover.append(crossover_top_bottom(selected_boards[board_indices[0]], selected_boards[board_indices[1]]))
        
        # Perform odd even crossover on one third of boards 
        else:
            boards_from_crossover.append(crossover_odd_even(selected_boards[board_indices[0]], selected_boards[board_indices[1]]))
    boards_from_crossover = np.asarray(boards_from_crossover)

    # Append boards from selection and boards from crossover to get final boards
    final_boards = np.vstack((boards_from_selection, boards_from_crossover))
    return final_boards