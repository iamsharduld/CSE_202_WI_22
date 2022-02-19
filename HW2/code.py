from collections import defaultdict
import random
from heapdict import heapdict
import math
import matplotlib.pyplot as plt

def plot_figure(x_array, x_array2=None, y_array=None):
    plt.plot(x_array, y_array, label="Average Case")
    plt.plot(x_array, x_array2, label="Worst Case")
    leg = plt.legend(loc='upper center')
    plt.title('Number of Decrease Key Operations vs Number of Vertices(n)')
    plt.ylabel('# of Decrease Key Operations')
    plt.xlabel('n')
    plt.show()


def plot_figure(x_array, x_array2=None, x_array3=None, y_array=None):
    plt.plot(x_array, y_array, label="Num of decrease key operations")
    plt.plot(x_array, x_array2, label="O(n)")
    plt.plot(x_array, x_array3, label="O(nlog(n))")

    leg = plt.legend(loc='upper center')
    plt.title('Number of Decrease Key Operations vs Number of Nodes(n)')
    plt.ylabel('Number of Decrease Key Operations')
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

    worst_case_ops = 0
    while len(priority_q) > 0:

        u, dist_u = priority_q.popitem()
        for neighbour_v in range(len(g[u])):
 
            dis = dist[u] + g[u][neighbour_v]
            worst_case_ops += 1

            if dis < dist[neighbour_v]:
                dist[neighbour_v] = dis
                prev[neighbour_v] = u
                priority_q[neighbour_v] = dis
                num_decrease_key_ops += 1
    return num_decrease_key_ops, worst_case_ops

y = []
x = []
x2 = []
x_log = []
line = []
for i in range(3,1000):
    x.append(i)
    ip_graph = build_graph(i)
    num_ops, worst_case_ops = djikstra(ip_graph,0)
    x2.append(worst_case_ops)
    x_log.append(i*math.log(i,2))
    line.append(i)
    y.append(num_ops)
    print(i, worst_case_ops)

print(x)
print(y)
# plot_figure(x,x2,y)
plot_figure(x,line,x_log,y)


