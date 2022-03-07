import numpy as np
import random

from src.utils import calculate_board_dim
from src.fitness import calculate_fitness

def crossover_left_right(board1, board2):
    """
        combines the left half of board1 with the right half of board2
    """
    # calculate dimensions of board 
    height, width = calculate_board_dim(board1)
    
    # initialize offsprings boards
    child_board_1, child_board_2 = np.zeros((height, width)), np.zeros((height, width))

    # find random crossover point to combine the parents
    idx = random.randint(0, width-1)

    child_board_1[:, : idx] = board1[:, : idx]
    child_board_1[:, idx:] = board2[:, idx:]

    child_board_2[:, : idx] = board2[:, : idx]
    child_board_2[:, idx:] = board1[:, idx:]

    return [child_board_1, child_board_2]

def crossover_top_bottom(board1, board2):
    """
        combines the top half of board1 with the bottom half of board2
    """
    # calculate dimensions of board 
    height, width = calculate_board_dim(board1)
    
    # initialize offsprings boards
    child_board_1, child_board_2 = np.zeros((height, width)), np.zeros((height, width))

    # find random crossover point to combine the parents
    idx = random.randint(0, height-1)

    child_board_1[: idx, :] = board1[: idx, :]
    child_board_1[idx:, :] = board2[idx:, :]

    child_board_2[: idx, :] = board2[: idx, :]
    child_board_2[idx:, :] = board1[idx:, :]
    
    return [child_board_1, child_board_2]

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

def crossover(boards, selection_perc):
    """
        combines three types of crossover to create a new generation 
    """
    # Select selction_ratio boards from selection
    num_boards = boards.shape[0]

    # calculate fitness score of all boards
    fitness_score = np.zeros((num_boards, ))
    for i in range(num_boards):
        fitness_score[i] = calculate_fitness(boards[i])

    fitness_score = 1 - fitness_score/np.sum(fitness_score)
    fitness_score = fitness_score/np.sum(fitness_score)

    #Selecting parents for crossover based on weighted fitness as probabilites
    selected_indices = np.random.choice(num_boards, int(selection_perc*0.01*num_boards), p=fitness_score)
    boards_from_selection = boards[selected_indices]
    
    # Peform crossover
    boards_from_crossover = []
    for i in range(int(boards_from_selection.shape[0]/2)):

        # Select 2 random indices from unselected indices
        board_indices = (2*i, 2*i+1) #np.random.choice(unselected_indices, 2, replace=False)
        
        crossover_method_idx = random.randint(0,1)
        if crossover_method_idx == 0:
            boards_from_crossover += crossover_left_right(boards[board_indices[0]], boards[board_indices[1]])
        else:
            boards_from_crossover += crossover_top_bottom(boards[board_indices[0]], boards[board_indices[1]])

    boards_from_crossover = np.asarray(boards_from_crossover)

    # Append boards from selection and boards from crossover to get final boards
    #final_boards = np.vstack((boards_from_selection, boards_from_crossover))
    return boards_from_crossover #final_boards