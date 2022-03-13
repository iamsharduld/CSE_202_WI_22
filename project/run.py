import numpy as np 
import random
import time

from src.validate import validate_board
from src.initialize import initialize
from src.selection import selection
from src.crossover import crossover
from src.mutation import mutation
from src.boards import boards

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
    
    # Abort after ABORT_GENERATIONS 
    ABORT_GENERATIONS = 10000

    # Initialize after REPLACE_GENERATIONS
    REPLACE_GENERATIONS = 500

    # Fraction of boards selected to the next generation
    alpha = 0.1

    # probability of mutation
    rho = 0.01

    # fraction of boards selcted for mutation
    beta = 0.01

    # Flag set true when solution is found
    success_flag = False

    # store average times taken to solve a particular board size
    times = []

    # store average generations taken to solve a particular board size
    generations = []
    
    # iterate using boards in boards.py
    for board_type in boards:
        # calculate average time for each board type
        time_per_board_size = 0

        # calulate generations for each board type
        generations_per_board_size = 0
        
        for k in range(len(board_type)):
            print("\n")

            # Reset success flag for each board
            success_flag = False

            for i in range(ABORT_GENERATIONS):
                # Initalize population after every REPLACE_GENERATIONS iterations
                if i % REPLACE_GENERATIONS == 0:
                    init_board = np.asarray(board_type[k])
                    print("The initial board is: \n", init_board)
                    
                    # record start time of run 
                    start_time  = time.time()
                    generated_boards = initialize(init_board)
                    print('#### Run:',int(i / REPLACE_GENERATIONS))

                # Perform selection
                selected_boards = selection(generated_boards, alpha) 

                # Perform crossover
                crossover_boards = crossover(generated_boards, 1 - alpha)
                all_boards = np.vstack((selected_boards, crossover_boards))
                
                # Perform mutation
                if random.uniform(0,1) < rho:
                    mutated_boards = mutation(all_boards, beta) 
                else:
                    mutated_boards = all_boards.copy()
                
                # validate
                for board in all_boards:
                    if validate_board(board) == True:
                        # record end time of run
                        end_time = time.time()

                        # calculate average time per board size
                        time_per_board_size = time_per_board_size + (end_time - start_time) / len(board_type)
                        
                        # calculate average generations per board size
                        generations_per_board_size = generations_per_board_size + i / len(board_type)

                        # set success_flag true when solution is found
                        success_flag = True
                        print("The solution is: \n",  board)
                        break
                if success_flag == True:
                    break

                print('GENERATION %d'%(i%REPLACE_GENERATIONS))
                print(generated_boards.shape, selected_boards.shape, crossover_boards.shape, mutated_boards.shape)
                
                generated_boards = mutated_boards.copy()
                
        
        # append average generations per board size to list
        print("Generations taken for board size: ", round(generations_per_board_size))
        generations.append(round(generations_per_board_size))

        # append average time taken per board size to list
        print("Time taken for board size: ", round(time_per_board_size, 3))    
        times.append(round(time_per_board_size, 3))

if __name__ == "__main__":
    main()