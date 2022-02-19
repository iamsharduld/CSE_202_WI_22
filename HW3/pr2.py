from collections import defaultdict
import math
import random
import matplotlib.pyplot as plt
import timeit

def plot_figure(x_array, y_array, is_bipartite=False):
    plt.plot(x_array, y_array)
    plt.title('Time vs Num Nodes')

    plt.ylabel('Time')
    plt.xlabel('Num Nodes')
    plt.show()

def plot_figure2(x_array, x_array2=None, x_array3=None, y_array=None):
    plt.plot(x_array, y_array, label="Num of decrease key operations")
    plt.plot(x_array, x_array2, label="O(n)")
    plt.plot(x_array, x_array3, label="O(nlog(n))")

    leg = plt.legend(loc='upper center')
    plt.title('Number of Decrease Key Operations vs Number of Nodes(n)')
    plt.ylabel('Number of Decrease Key Operations')
    plt.xlabel('n')
    plt.show()

def solve(n, m):
    # print(n)
    x = defaultdict(list)
    for ele in m:

        x[ele[1]].append(ele)
    # print(x)
    for k in x:
        x[k].sort()
    # print(x)
    
    fin = []
    for i in range(n+1):
        if len(x[i]) > 0:
            fin += x[i]
    # print(fin)
    gn = 0
    arr = [0 for i in range(n)]
    j = 0
    i = 0
    cnt = 0
    while i < n and j < len(fin):
        gn += 1
        # print(i,fin)
        if len(fin) > j:
            ele = fin[j]
   
        a = i + 1
        if ele[0] <= a and ele[1] >= a:
            # print("here")
            arr[i] = ele[2]
            j += 1
            cnt += 1
        elif ele[1] < a:
            j += 1
            # i -= 1
            continue
        i += 1

        
    # print(j)
    # print(arr)

    cnt += 1
    return gn


avail_movies = defaultdict(list)
n = random.randint(7,13)

p = [(1, 2, 'd'), (1, 2, 'f'), (2, 2, 'c'), (3, 3, 'e'), (2, 5, 'a'), (3, 6, 'b'), (4, 6, 'g'), (4, 7, 'h')]
b = [(2, 3, 'd'), (1, 5, 'f'), (3, 5, 'b'), (3, 5, 'i'), (2, 6, 'e'), (3, 9, 'a'), (9, 9, 'h'), (3, 10, 'g'), (7, 10, 'c'), (7, 10, 'j')]
c = [(3,6,'a'),(3,6,'b'),(3,6,'c'),(3,6,'d'),(3,6,'e'),(1,8,'f')]
time_plot = []
n_arr = []
nlogn = []
num_ops = []
for y in range(10, 1500):

    arr = []
    x = [random.randint(1,1000000) for i in range(y)]

    for i in range(len(x)):
        a = random.randint(1,n)
        b = random.randint(1,n)
        while b < a:
            # print(a,b)
            a = random.randint(1,n)
            b = random.randint(1,n)
            continue
        arr.append((a,b, x[i]))
    print(y)
        # avail_movies[x[i]] += [a, b]
    ops = solve(y, arr)
    num_ops.append(ops)
    # t = timeit.timeit(lambda: solve(y, arr), number=1)
    # time_plot.append(t)
    n_arr.append(y)
    nlogn.append(n*math.log(n))
print(time_plot)
print(n_arr)
# plot_figure(n_arr, num_ops)
plot_figure2(n_arr,  nlogn, num_ops, num_ops)