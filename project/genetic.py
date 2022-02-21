import numpy as np 
import random

def neighbor_directions():
    """
        defines neighbor directions - left, top, right, down
    """
    dx = [0, -1, 0, 1]
    dy = [-1, 0, 1, 0]
    return dx, dy

def is_valid(row, col, height, width):
    """
        returns true if an index [row, col] is valid, otherwise false
    """
    return row >= 0 and row < height and col >= 0 and col < width

def calculate_board_dim(board):
    """
        calculates the dimensions of a board
    """
    return board.shape[0], board.shape[1]

def dfs(board, visited, row, col, height, width):
    """
        starts from white cell [row, col] and checks that all white cells form a connected graph
    """
    # mark current cell as visited
    visited[row, col] = 1
    print(row, col)
    # define neighbor directions - left, up, right, down
    dx = [0, -1, 0, 1]
    dy = [-1, 0, 1, 0]

    # perform dfs on white cells
    for k in range(4):
        if is_valid(row + dx[k], col + dy[k], height, width) and visited[row + dx[k], col + dy[k]] == 0 and board[row + dx[k], col + dy[k]] != -1:
            #print(row + dx[k], col + dy[k])
            dfs(board, visited, row + dx[k], col + dx[k], height, width)

def calculate_adjacent_black_cells(board):
    """
        calculates the number of adjacent black cells in a board
    """
    # get neighbor directions 
    dx, dy = neighbor_directions()

    # get board dimensions 
    height, width = calculate_board_dim(board)

    # calculate adjacent black cells
    adjacent_black_cells = 0
    for i in range(height):
        for j in range(width):
            for k in range(4):
                # check how many neighbor cells of a black cell are black
                if is_valid(i - dx[k], j - dy[k], height, width) and board[i, j] == -1 and board[i - dx[k], j - dy[k]] == -1:
                    adjacent_black_cells += 1
    return adjacent_black_cells

def calculate_connected_components(board):
    """
        calculates the number of connected components formed by white cells in a given board
    """
    # get neighbor directions 
    dx, dy = neighbor_directions()

    # get board dimensions 
    height, width = calculate_board_dim(board)

    # calculate connected components 
    st = []
    visited = np.zeros((height, width), np.int32)
    connected_components = 0

    # perform dfs to calculate the connected components in graph
    for i in range(height):
        for j in range(width):
            if board[i, j] != -1 and visited[i, j] == 0: 
                connected_components += 1
                st.append([i, j])
                visited[i, j] = 1
                while(st):
                    row, col = st.pop()
                    for k in range(4):
                        if is_valid(row + dx[k], col + dy[k], height, width) and visited[row + dx[k], col + dy[k]] == 0 and board[row + dx[k], col + dy[k]] != -1:
                            st.append([row + dx[k], col + dy[k]])
                            visited[row + dx[k], col + dy[k]] = 1

    return connected_components

def calculate_visible_cells(board, row, col):
    """
        calculates the visible white cells from [row, col]
    """
    # get board dimensions 
    height, width = calculate_board_dim(board)

    # initialize visible_cells to 1 as the definition includes the cell itself
    visible_cells = 1
    
    # check left
    j = col - 1
    while(j >= 0 and board[row, j] != -1):
        j -= 1
        visible_cells += 1
    
    # check up
    i = row - 1 
    while(i >= 0 and board[i, col] != -1):
        i -= 1
        visible_cells += 1
    
    # check right
    j = col + 1
    while(j < width and board[row, j] != -1):
        j += 1
        visible_cells += 1
    
    # check down
    i = row + 1
    while(i < height and board[i, col] != -1):
        i += 1
        visible_cells += 1
    
    return visible_cells

def calculate_absolute_differences(board):
    """
        calculates the sum of absolute diffrences between white cells visible from numbered cells and actual number on cells
    """
    f2 = 0

    # find numbered cell indices 
    numbered_cell_indices = np.argwhere(board > 0)

    for r, c in numbered_cell_indices:
        # calculate visible cells from each numbered cell 
        visible_cells = calculate_visible_cells(board, r, c)

        # find absolute difference between visible cells from a numbered cell and actual number on cell 
        f2 += abs(board[r, c] - visible_cells)
    return f2

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
    print("Constraint 1 passed ")
    
    # check that all white cells are connected 
    connected_components = calculate_connected_components(board)
    if connected_components != 1:
        return False

    print("Constraint 2 passed ")

    # check that the numbered cells are numbered correctly 
    numbered_cell_indices = np.argwhere(board > 0)
    for r, c in numbered_cell_indices:
        visible_cells = calculate_visible_cells(board, r, c)
        if visible_cells != board[r, c]:
            return False

    print("Constraint 3 passed")    
    return True


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

def vanilla_selection(boards, num_selected=100):
    """
        selects the fittest num_selected boards from an array of boards
    """
    # calculate dimensions of board 
    height, width = calculate_board_dim(boards[0])

    # calculate number of boards from which selection is to be done
    num_boards = boards.shape[0]

    # select num_selected boards using vanilla method
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
    selected_boards_tournament = tournament_selection(boards, num_selected)
    selected_boards = np.vstack((selected_boards_vanilla, selected_boards_tournament))
    return selected_boards

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

    # extract odd rows of board1 and assign to odd rows of new board
    new_board[1::2] = board1[1::2]
    return new_board

# TODO define crossover function
def crossover():
    """
        combines three types of crossover to create a new generation 
    """
    pass

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

    # calculate adjacent black cells
    adjacent_black_cells = 0
    for i in range(height):
        for j in range(width):
            for k in range(4):
                # if neighbor of black cell is black, make it white
                if is_valid(i + dx[k], j + dy[k], height, width) and board[i, j] == -1 and board[i + dx[k], j + dy[k]] == -1:
                    board[i + dx[k], j + dy[k]] = 1
    return adjacent_black_cells

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

def random_mutation(board, black_to_white_ratio=0.1, white_to_black_ratio=0.1):
    """
        random flips black cells to white and vice versa
    """
    # find black and white cell indices in original board 
    black_cell_indices = np.argwhere(board == -1)
    white_cell_indices = np.argwhere(board == 0)

    # find number of black and white cells on board
    num_black_cells = black_cell_indices.shape[0]
    num_white_cells = white_cell_indices.shape[0]

    # find number of black and white cells to flip
    num_flipped_black_cells = int(black_to_white_ratio * num_black_cells)
    num_flipped_white_cells = int(white_to_black_ratio * num_white_cells)

    # randomly flip black cells to white
    black_to_white_indices = random.sample(range(num_black_cells), num_flipped_black_cells)
    for i in range(len(black_to_white_indices)):
        board[black_cell_indices[black_to_white_indices[i]]] = 0

    # randomly flip white cells to black
    white_to_black_indices = random.sample(range(num_white_cells), num_flipped_white_cells)
    for i in range(len(white_to_black_indices)):
        board[white_cell_indices[white_to_black_indices[i]]] = -1
    
    return board

# TODO write mutation function
def mutation():
    """
        combines three types of mutation to create mutations in a generation
    """
    pass 

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
    init_board = np.array([[0, 0, 3, 0, 0],
                    [9, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0],
                    [0, 2, 0, 0, 2],
                    [0, 0, 0, 0, 0]], np.int32)  
    # random_boards = initialize(init_board)
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


if __name__ == "__main__":
    main()
