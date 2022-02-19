from collections import defaultdict
import random
from itertools import permutations

def comma_sep_adj_mat(g):
    for i in range(len(g)):
        for j in range(len(g[i])):
            if j != len(g[i])-1:
                print(str(g[i][j]) + ", ", end="", flush=True)
            else:
                print(str(g[i][j]), end="", flush=True)

        print()

def build_graph(n):
    g = [[0 for i in range(n)] for j in range(n)]

    for i in range(n):
        for j in range(n):

            if i == j:
                if i == j:
                    g[i][j] = 0
                continue
            if random.randint(0,1):
                edge_weight = random.randint(1,13)
                g[i][j] = edge_weight
            if random.randint(0,1):
                edge_weight = random.randint(1,13)
                g[j][i] = edge_weight

    # g = [[0, 5, 0, 10], [0, 0, 3, 10], [9, 13, 0, 0], [0, 5, 11, 0]]
    comma_sep_adj_mat(g)
    return g

# 3 2 4 1
def brutest_force(g):
    n = len(g)
    
    arr = [i for i in range(n)]
    # print(arr)
    itr = permutations(arr,len(arr))
    ans = defaultdict(int)
    for i in itr:
        # print(i)
        perm = i
        tmp = 0
        for j in range(n):
            for k in range(j+1,n):
                tmp += g[perm[j]][perm[k]]
        ans[i] = tmp
    ans_key = min(ans, key=ans.get)
    ans_val = ans[ans_key]
    for i in ans:
        print(i, ans[i])
    return ans_key, ans_val
    # return ans

def efficient(g):
    degree_of_nodes = defaultdict(int)
    fwd_degree = defaultdict(int)

    incoming_edge_sum = defaultdict(int)
    for i in range(len(g)):
        for j in range(len(g)):
            incoming_edge_sum[i] += g[j][i]
            if g[i][j] != 0:
                degree_of_nodes[i] += 1
                fwd_degree[i] += 1
            if g[j][i] != 0:
                degree_of_nodes[i] += 1


    print("incoming", incoming_edge_sum)

    outgoing_weight = defaultdict(int)
    for i in range(len(g)):
        for j in range(len(g)):
            outgoing_weight[i] += g[i][j]
    print("outgoing", outgoing_weight)

    ratio_weights = defaultdict(int)
    for i in outgoing_weight:
        ratio_weights[i] += incoming_edge_sum[i]/float(outgoing_weight[i])
    print("ratio weights", ratio_weights)
    print("node degree", degree_of_nodes)
    print("Forward degree",fwd_degree )
    

    # Ratio? outgoing / incoming
    return g





bg = build_graph(5)
print(brutest_force(bg))
efficient(bg)


