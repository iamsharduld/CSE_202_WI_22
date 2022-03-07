import numpy as np 
import random

from src.validate import validate_board
from src.initialize import initialize
from src.selection import selection
from src.crossover import crossover
from src.mutation import mutation

def main():
    # uncomment to take input
    # rows = int(input("Enter number of rows: "))
    # cols = int(input("Enter number of cols: "))
    
    # board = []
    # print("Enter the initial board row wise: ")
    # for i in range(rows):
    #     row = list(map(int, input().split()))
    #     board.append(row)
    # board = np.asarray(board)

    # Define initial test board
    init_board = np.array([[0, 0, 3, 0, 0],
                    [9, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0],
                    [0, 2, 0, 0, 2],
                    [0, 0, 0, 0, 0]], np.int32)  

    init_board = np.array([[0, 6, 10, 0, 0, 3, 0],
                    [0, 0, 0, 0, 9, 0, 0],
                    [0, 0, 9, 0, 4, 0, 0], 
                    [4, 0, 11, 7, 8, 0, 7],
                    [0, 0, 12, 0, 9, 0, 0],
                    [0, 0, 8, 0, 0, 0, 0],
                    [0, 3, 0, 0, 3, 6, 0]], np.int32)
    
    # init_board = np.array([[4, 0, 5, 0, 0],
    #                    [6, 0, 0, 0, 0],
    #                    [0, 0, 0, 0, 7],
    #                    [0, 0, 0, 0, 5]], np.int32)

    BOARD_5x4 = [np.array([[4, 0, 5, 0, 0],
                       [6, 0, 0, 0, 0],
                       [0, 0, 0, 0, 7],
                       [0, 0, 0, 0, 5]]),
             np.array([[0, 0, 0, 0, 4],
                       [0, 7, 8, 0, 0],
                       [0, 0, 7, 6, 0],
                       [5, 0, 0, 0, 0]]),
             np.array([[0, 6, 0, 0, 0],
                       [0, 6, 7, 0, 0],
                       [0, 0, 4, 5, 0],
                       [0, 0, 0, 5, 0]])]

    test_board_1 = np.array([[0, 0, 3, 0, 0],
                    [-1, -1, -1, -1, -1],
                    [0, 0, -1, 0, 0],
                    [0, 2, 0, 0, 2],
                    [0, 0, 0, 0, 0]], np.int32) 
    
    sol_board = np.array([[0, -1, 3, -1, 0],
                    [9, 0, 0, 0, 0],
                    [0, -1, 0, 0, -1],
                    [0, 2, -1, 0, 2],
                    [0, -1, 0, 0, -1]], np.int32)
    
    # Abort after ABORT_GENERATIONS 
    ABORT_GENERATIONS = 10000

    # Initialize after REPLACE_GENERATIONS
    REPLACE_GENERATIONS = 500

    # Flag set true when solution is found
    success_flag = False

    for i in range(ABORT_GENERATIONS):
        # Initalize population after every REPLACE_GENERATIONS iterations
        if i % REPLACE_GENERATIONS == 0:
            generated_boards = initialize(init_board)
            print('#### Run:',int(i/REPLACE_GENERATIONS))

        selection_ratio = 10
        # Perform selection
        selected_boards = selection(generated_boards, selection_ratio) #250)
        

        # Perform crossover
        crossover_boards = crossover(generated_boards, 100-selection_ratio)
        all_boards = np.vstack((selected_boards, crossover_boards))
        
        # Perform mutation
        if random.uniform(0,1) < 0.01:
            mutated_boards = mutation(all_boards, mutation_perc=1) #crossover_boards)
        else:
            mutated_boards = all_boards.copy()
        
        # validate
        for board in all_boards:
            if validate_board(board) == True:
                success_flag = True
                print("The solution is")
                print(board)
                break
        if success_flag == True:
            break

        print('GENERATION %d'%(i%REPLACE_GENERATIONS))
        print(generated_boards.shape, selected_boards.shape, crossover_boards.shape, mutated_boards.shape)

        generated_boards = mutated_boards.copy()
if __name__ == "__main__":
    main()