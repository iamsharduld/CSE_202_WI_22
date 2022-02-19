import matplotlib.pyplot as plt
import random
from collections import defaultdict

import timeit
import math


def build_graph(n):

    # given = {(0, 2): 1, (0, 3): 6, (0, 4): 4, (1, 3): 13, (2, 0): 12, (2, 4): 2, (3, 1): 1, (4, 0): 5, (4, 2): 14, (4, 3): 9}
    given = None
    g = defaultdict(int)
    adj_list = defaultdict(set)
    if given:
        for key in given:
            g[key] = given[key]
            adj_list[key[0]].add(key[1])
        return g, adj_list
    num_edges = 0
    for i in range(n):
        for j in range(n):
            if i == j:
                continue
            a = random.randint(0,1)
            if a:
                g[(i,j)] = random.randint(1,15)
                adj_list[i].add(j)
                num_edges += 1
                # g[j][i] = edge_weight
    # print("num edges", num_edges)
    return g,adj_list

# https://graphonline.ru/en/create_graph_by_matrix

def monotonic_path(g, adj_list):
    visited = defaultdict(bool)
    # print("g", g)
    for i in g:
        # print(g[i])
        visited[i] = False

    # print(visited)
    # return

    st = []
    st.append(0)
    prev = -1

    while len(st) != 0:
        ver = st.pop()
        # print("prev", prev+1, "ver", ver+1)

        for adj_ver in adj_list[ver]:
            # print("prev=", prev+1, "Curr=", ver+1, "adj_ver", adj_ver+1, "distances", g[(prev, ver)],g[(ver, adj_ver)])
            if not visited[(ver, adj_ver)] and g[(prev, ver)] < g[(ver, adj_ver)]:
                # print(ver+1, adj_ver+1)
                visited[(ver, adj_ver)] = True
                prev = ver
                st.append(adj_ver)

                if adj_ver == 1:
                    return True
            
            # if g[(prev, ver)] > g[(ver, adj_ver)]:
            #     print("Weight exceeded", prev+1, ver+1, adj_ver+1)
                # visited[(ver, adj_ver)] = True


    # print("len",len(visited))

    return False


def plot_figure(x_array, y_array, is_bipartite=False):
    plt.plot(x_array, y_array)
    plt.title('Time vs Num Nodes')

    plt.ylabel('Time')
    plt.xlabel('Num Nodes')
    plt.show()

time1 = []
nums = []
for i in range(3, 500):
    print(i)
    n = i
    g, adj_list = build_graph(n)
    t = timeit.timeit(lambda: monotonic_path(g, adj_list), number=10)
    # print(t)
    nums.append(math.log(i,2))
    time1.append(math.log(t,2))
    # monotonic_path(g, adj_list)
plot_figure(nums,time1)
# print(monotonic_path(g, adj_list))

# cpy = [[0 for i in range(n)] for j in range(n)]

# for i in g:
#     st,en = i[0],i[1]
#     # print("here",i)
#     cpy[st][en] = g[(i[0],i[1])]

# for i in range(len(cpy)):
#     for j in range(len(cpy[i])):
#         if j != len(cpy[i])-1:
#             print(str(cpy[i][j]) + ", ", end="", flush=True)
#         else:
#             print(str(cpy[i][j]), end="", flush=True)

#     print()
