import numpy as np
import random

from src.utils import calculate_board_dim
from src.fitness import calculate_fitness

def vanilla_selection(boards, alpha=0.01):
    """
        selects the fittest aplha fraction of boards from an array of boards
    """
    # calculate dimensions of board 
    height, width = calculate_board_dim(boards[0])

    # calculate number of boards from which selection is to be done
    num_boards = boards.shape[0]

    # select perc_selected*num_boards boards using vanilla method
    num_selected = int(alpha * num_boards)
    selected_boards_vanilla = np.zeros((num_selected, height, width))

    # calculate fitness score of all boards
    fitness_score = np.zeros((num_boards, ))
    for i in range(num_boards):
        fitness_score[i] = calculate_fitness(boards[i])
    
    # select fittest num_selected boards
    selected_indices_vanilla = np.argsort(fitness_score)[: num_selected]
    selected_boards_vanilla = boards[selected_indices_vanilla]

    return selected_boards_vanilla

def tournament_selection(boards, num_selected=100):
    """
        selects num_selected boards using tournament method
        forms num_selected random groups and selects fittest from each group
    """
    # calculate dimensions of board 
    height, width = calculate_board_dim(boards[0])

    # calculate number of boards from which selection is to be done
    num_boards = boards.shape[0]

    # select num_selected boards using vanilla method
    selected_boards_tournament = np.zeros((num_selected, height, width))

    # randomize indices in range
    random_indices = random.sample(range(num_boards), num_boards)
    
    # calculate the number of boards in each group
    num_boards_in_group = int(num_boards / num_selected)

    # define list to store index of fittest board in each group
    fittest_indices_tournament = []

    for i in range(num_selected):
        # choose indices of boards in each group
        board_indices_in_group = random_indices[i * num_boards_in_group : min((i + 1) * num_boards_in_group, num_boards)]
        fitness_score = np.zeros((len(board_indices_in_group), ))

        # calculate fitness score for each board in group
        for j in range(len(board_indices_in_group)):
            fitness_score[j] = calculate_fitness(boards[board_indices_in_group[j]])
        
        # store the index of the fittest board in each group
        fittest_indices_tournament.append(np.argsort(fitness_score)[0])
    
    selected_indices_tournament = np.asarray(fittest_indices_tournament)

    # return the fittest boards in each group
    selected_boards_tournament = boards[selected_indices_tournament]
    return selected_boards_tournament


def selection(boards, num_selected=100):
    """
        concatenates the boards selected by vanilla and tournament selection
    """
    selected_boards_vanilla = vanilla_selection(boards, num_selected)
    #selected_boards_tournament = tournament_selection(boards, num_selected)
    #selected_boards = np.vstack((selected_boards_vanilla, selected_boards_tournament))
    return selected_boards_vanilla