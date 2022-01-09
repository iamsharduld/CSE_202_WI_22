import random

import matplotlib.pyplot as plt
import math

def graph_generator(num_vertices):
    # print(num_vertices)
    g = []

    for i in range(num_vertices):
        
        tmp = []

        for j in range(num_vertices):
            prob = random.randint(0, 1)
            tmp.append(prob)

        g.append(tmp)
    # print(g)
    return g

def plot_figure(x_array, y_array):
    plt.plot(x_array, y_array)   
    # print("C2H5OH".translate(subscript)) 

    plt.ylabel('$\mathregular{Log_{10}}$(Time)')
    plt.xlabel('$\mathregular{Log_{2}}$(N)')
    plt.show()


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
two_power = []
algo1_time = []
algo2_time = []

for i in range(2,12):
    temp_t1 = []
    temp_t2 = []
    print("Graph generated for Num Nodes=",2**i)
    for gr in range(20):
        graph = graph_generator(2**i)
        n = len(graph)
        t1 = timeit.timeit(lambda: brute_force(graph), number=1)
        t2 = timeit.timeit(lambda: optimal(graph), number=1)
        temp_t1.append(t1)
        temp_t2.append(t2)
    
    avg_t1 = sum(temp_t1)/float(len(temp_t1))
    avg_t2 = sum(temp_t2)/float(len(temp_t2))

    two_power.append(i)
    algo1_time.append(math.log(avg_t1,10))
    algo2_time.append(math.log(avg_t2,10))


print(two_power)
print(algo1_time)
print(algo2_time)

plot_figure(two_power, algo1_time)
plot_figure(two_power, algo2_time)