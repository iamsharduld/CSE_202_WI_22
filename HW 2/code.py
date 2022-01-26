from collections import defaultdict
import random
from heapdict import heapdict
import math
import matplotlib.pyplot as plt

def plot_figure(x_array, y_array):
    plt.plot(x_array, y_array)
    plt.title('Number of Vertices(n) vs Number of Decrease Operations')
    plt.ylabel('# of Decrease Operations')
    plt.xlabel('n')
    plt.show()

def build_graph(n):

    g = [[-1 for i in range(n)] for j in range(n)]

    for i in range(n):
        for j in range(n):

            if i == j or g[i][j] != -1:
                if i == j:
                    g[i][j] = 0
                continue
           
            edge_weight = random.uniform(0,1)
            g[i][j] = edge_weight
            g[j][i] = edge_weight
    
    return g

def print_q(q):

    for i in q:
        print(i, q[i])
    print()

def djikstra(g, source):

    num_decrease_key_ops = 0

    n = len(g)

    dist = [0 for i in range(n)]
    prev = [0 for i in range(n)]

    dist[source] = 0
    priority_q = heapdict()

    for v in range(n):
        if v != source:
            dist[v] = math.inf
            prev[v] = None

        priority_q[v] = dist[v]


    while len(priority_q) > 0:

        u, dist_u = priority_q.popitem()
        for neighbour_v in range(len(g[u])):
 
            dis = dist[u] + g[u][neighbour_v]

            if dis < dist[neighbour_v]:
                dist[neighbour_v] = dis
                prev[neighbour_v] = u
                priority_q[neighbour_v] = dis
                num_decrease_key_ops += 1
    return num_decrease_key_ops

y = []
x = []
for i in range(3,1000):
    x.append(i)
    ip_graph = build_graph(i)
    num_ops = djikstra(ip_graph,0)
    y.append(num_ops)
    print(i)

print(x)
print(y)
plot_figure(x,y)