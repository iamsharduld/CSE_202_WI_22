V = [[0,1,0], [1,1,1], [1,0,1]]

def graph_generator(num_vertices):
    print(num_vertices)
    g = []

    for i in range(num_vertices):
        
        tmp = []

        for j in range(num_vertices):
            prob = random.randint(0, 1)
            tmp.append(prob)

        g.append(tmp)
    print(g)
    return g



# Algorithm 1
# O(V^3)

def brute_force(graph):
    ### Adjacency Matrix input

    num_vertices = len(graph)

    for i in range(num_vertices):
        for j in range(num_vertices):
            if i == j:
                continue
            for k in range(num_vertices):
                if i == k or j == k:
                    continue
                
                if graph[i][j] == 1 and graph[i][k] == 1 and graph[j][k] == 1:
                    return True
        
    return False


# Algorithm 2
# O(V^2 + V.E)

def optimal(graph):

    num_vertices = len(graph)
    edges = []

    for i in range(num_vertices):
        for j in range(num_vertices):
            if graph[i][j] == 1:
                edges.append((i,j))
    
    for edge in edges:
        for vert in range(num_vertices):
            if vert == edge[1] or vert == edge[0]:
                continue
            if graph[edge[1]][vert] == 1 and graph[edge[0]][vert] == 1:
                return True
    return False


import timeit

for i in range(2,10):
    
    graph = graph_generator(2**i)
    n = len(graph)
    t1 = timeit.timeit(lambda: brute_force(graph), number=1)
    t2 = timeit.timeit(lambda: optimal(graph), number=1)


print(brute_force(V))





