import numpy as np 

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
        
        # Perform selection and validate
        selected_boards = selection(generated_boards, 250)
        for board in selected_boards:
            if validate_board(board) == True:
                success_flag = True
                print("The solution is")
                print(board)
                break
        if success_flag == True:
            break

        # Perform crossover and validate
        crossover_boards = crossover(selected_boards, 0.17)
        for board in crossover_boards:
            if validate_board(board) == True:
                success_flag = True
                print("The solution is")
                print(board)
                break
        if success_flag == True:
            break

        # Perform mutation and validate
        mutated_boards = mutation(crossover_boards)
        for board in mutated_boards:
            if validate_board(board) == True:
                success_flag = True
                print("The solution is")
                print(board)
                break
        if success_flag == True:
            break

if __name__ == "__main__":
    main()