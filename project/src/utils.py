import numpy as np

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