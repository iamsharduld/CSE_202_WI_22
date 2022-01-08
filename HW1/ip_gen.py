import random


for t in range(4):

    num_vertices = random.randint(5*(10**t),10*(10**t))
    print(num_vertices)
    g = []

    for i in range(num_vertices):
        
        tmp = []

        for j in range(num_vertices):
            prob = random.randint(0, 1)
            tmp.append(prob)

        g.append(tmp)
    print(g)
