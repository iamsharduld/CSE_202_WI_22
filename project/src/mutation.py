import numpy as np
import random 

from src.utils import calculate_board_dim, neighbor_directions, is_valid, calculate_absolute_differences

# TODO add randomness 
def adjacent_cell_mutation(board):
    """
        ensures that a board doesn't have two adjacent black cells
        if there are 2 adjacent black cells, one is made white
    """
    # get neighbor directions 
    dx, dy = neighbor_directions()

    # get board dimensions 
    height, width = calculate_board_dim(board)

    # make adjacent black cell white
    for i in range(height):
        for j in range(width):
            for k in range(4):
                # if neighbor of black cell is black, make it white
                if is_valid(i + dx[k], j + dy[k], height, width) and board[i, j] == -1 and board[i + dx[k], j + dy[k]] == -1:
                    board[i + dx[k], j + dy[k]] = 1
    return board

def absolute_difference_mutation(board):
    """
        removes black cells that don't contribute to absolute difference of the board 
    """
    # calculate f2 for given board
    original_difference = calculate_absolute_differences(board)

    # find black cell indices
    black_cell_indices = np.argwhere(board == -1)

    for r, c in black_cell_indices:
        # set each black cell as white
        board[r, c] = 0
        # calculate f2 for changed board
        curr_difference = calculate_absolute_differences(board)
        # set cell black only if it contributes to f2
        if original_difference != curr_difference:
            board[r, c] = -1
    
    return board

def random_mutation(board, gamma=0.1):
    """
        random flips gamma fraction black cells to white and vice versa
    """
    # find black and white cell indices in original board 
    black_cell_indices = np.argwhere(board == -1)
    white_cell_indices = np.argwhere(board == 0)

    # find number of black and white cells on board
    num_black_cells = black_cell_indices.shape[0]
    num_white_cells = white_cell_indices.shape[0]

    # find number of black and white cells to flip
    num_flipped_black_cells = int(gamma * num_black_cells)
    num_flipped_white_cells = int(gamma * num_white_cells)
    
    # randomly flip black cells to white
    black_to_white_indices = random.sample(range(num_black_cells), num_flipped_black_cells)
    if num_flipped_black_cells > 0:
        for i in range(len(black_to_white_indices)):
            board[tuple(black_cell_indices[black_to_white_indices[i]])] = 0

    # randomly flip white cells to black
    white_to_black_indices = random.sample(range(num_white_cells), num_flipped_white_cells)
    if num_flipped_white_cells > 0:
        for i in range(len(white_to_black_indices)):
            board[tuple(white_cell_indices[white_to_black_indices[i]])] = -1
        
    return board

def mutation(crossover_boards, beta=0.01):
    """
        creates mutations in a generation
    """
    # Calculate number of boards
    num_boards = crossover_boards.shape[0]

    # get board dimensions 
    height, width = calculate_board_dim(crossover_boards[0])
    
    #Selecting parents for crossover based on weighted fitness as probabilites
    selected_indices = np.random.choice(num_boards, int(beta * num_boards))
    
    
    for select_board_idx in selected_indices:
        crossover_boards[select_board_idx] = random_mutation(crossover_boards[select_board_idx])

    # mutated_boards = np.zeros((num_boards, height, width))
    # # Perfrom mutation on selected boards with proability 0.5
    # for i in range(num_boards):
        # Flag to that says if board is to be mutated
        # flag_perform_mutation = random.randrange(100)

        # if flag_perform_mutation % 2 == 1:
            # Flag that specifies the type of mutation
            # flag_mutation_type = random.randrange(300)
            # if flag_mutation_type % 3 == 0:
            #     mutated_boards[i] = adjacent_cell_mutation(selected_boards[i])
            # elif flag_mutation_type % 3 == 1:
            #     mutated_boards[i] = absolute_difference_mutation(selected_boards[i])
            # else:
        # mutated_boards[i] = random_mutation(selected_boards[i])
        # else:
        #     mutated_boards[i] = selected_boards[i]
    
    return crossover_boards #mutated_boards