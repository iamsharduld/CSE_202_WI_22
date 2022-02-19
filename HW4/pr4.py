from collections import defaultdict
import matplotlib.pyplot as plt
import timeit
import random

import numpy as np

def plot_figure(x_array,
                x_label='X Label Placeholder',
                y_axis_label='Y Label Placeholder',
                y_array2=[],
                y2_label="",
                y_array3=[],
                y3_label="",
                optional=10):


    if len(y_array2) > 0:
        plt.plot(x_array, y_array2, label=y2_label)
    if len(y_array3) > 0:
        print("here")
        plt.plot(x_array, y_array3, label=y3_label)
   

    plt.text(optional, 1.1*y_array2[optional-1], "x = "+str(optional))
    plt.plot(optional, y_array2[optional-1], 'go')

    # leg = plt.legend(loc='upper center')
    plt.title('Time(s) VS Threshold')
    plt.ylabel(y_axis_label)
    plt.xlabel(x_label)
    plt.show()

def karatsuba(x, y, threshold=1):
    # print(x,y)
    if len(str(x)) <= threshold or len(str(y)) <= threshold:
        return naive_gradeschool(x,y)
    else:
        m = max(len(str(x)),len(str(y)))
        m2 = m // 2

        a = x // 10**(m2)
        b = x % 10**(m2)
        c = y // 10**(m2)
        d = y % 10**(m2)


        z0 = karatsuba(b,d,threshold)
        z1 = karatsuba((a+b),(c+d),threshold)
        z2 = karatsuba(a,c,threshold)

        return (z2 * 10**(2*m2)) + ((z1 - z2 - z0) * 10**(m2)) + (z0)

def naive_gradeschool(x, y):

    return gradeSchoolMultiplication(x, y)

def zeroPad(numberString, zeros, left = True):
    """Return the string with zeros added to the left or right."""
    for i in range(zeros):
        if left:
            numberString = '0' + numberString
        else:
            numberString = numberString + '0'
    return numberString
 
def gradeSchoolMultiplication(x, y):
    """Multiply two integers using the grade-school algorithm."""
    #convert to strings for easy access to digits
    x = str(x)
    y = str(y)
    #keep track of number of zeros required to pad partial multiplications
    zeroPadding = 0
    #sum the partial multiplications as we go
    partialSum = 0
    #loop over each digit in the second number
    for i in range(len(y) -1, -1, -1):
        #keep track of carry for multiplications resulting in answers > 9        
        carry = 0
        #partial multiplication answer as a string for easier manipulation
        partial = ''
        #pad with zeros on the right
        partial = zeroPad(partial, zeroPadding, False)
        #loop over each digit in the first number
        for j in range(len(x) -1, -1, -1):
            z = int(y[i])*int(x[j])
            z += carry
            #convert to string for easier manipulation
            z = str(z)
            #keep track of carry when answer > 9
            if len(z) > 1:
                carry = int(z[0])
            else:
                carry = 0
            #concatenate final answer to the left of partial string    
            partial = z[len(z) -1] + partial
        #if there's any carry left at the end concatenate to partial string
        if carry > 0:
            partial = str(carry) + partial
        #sum the partials as you go        
        partialSum += int(partial)
        #for the next digit of the second number we need another zero to the right
        zeroPadding += 1
    return partialSum


def naive_vs_karatsuba():

    karat_time = []
    naive_time = []
    input_size = []
    for i in range(1, 300):
        print(i)
        input_size.append(i)
        t1_list = []
        t2_list = []

        num_repeat = 25

        for j in range(num_repeat):
            x = random.randint(10**(i), 10**(i+1))
            y = random.randint(10**(i), 10**(i+1))
            # print(x,y)
            # ans1 = karatsuba(x,y)
            # ans2 = naive_gradeschool(x,y)
            t1 = timeit.timeit(lambda: karatsuba(x,y), number=1)
            t2 = timeit.timeit(lambda: naive_gradeschool(x,y), number=1)
            t1_list.append(t1)
            t2_list.append(t2)
        
        karat_time.append(sum(t1_list)/float(num_repeat))
        naive_time.append(sum(t2_list)/float(num_repeat))


    threshold_val = -1
    # Threshold is 8 on Mac OS 64 bit architecture

    for i in range(len(karat_time)):
        if karat_time[i] >= naive_time[i]:
            threshold_val = i
    print(threshold_val)
    params = defaultdict(int)
    plot_figure(input_size, x_label="Input Size", y_axis_label = "Time", y_array2 = karat_time, y2_label="Karatsuba", y_array3=naive_time, y3_label="Naive", optional=threshold_val)

def run_experiment(n_times, num_index, threshold):
    time_array = []

    for _ in range(n_times):
        x = random.randint(10**(num_index), 10**(num_index+1))
        y = random.randint(10**(num_index), 10**(num_index+1))
        t = timeit.timeit(lambda: karatsuba(x,y,threshold), number=1)
        time_array.append(t)

    an = float(sum(time_array)) / float(len(time_array))
    return an

def karatsuba_with_diff_thresholds():
    karat_time = defaultdict(list)
    x_axis = []
    for i in range(1,100):
        x_axis.append(i)
        print(i)

        for threshold in range(1,20,1):
            t = run_experiment(40, i, threshold)
            karat_time[threshold].append(t)
    
    for i in karat_time:
        plt.plot(x_axis, karat_time[i], label="Threshold = "+str(i))

    plt.title('Title')
    plt.ylabel("Time(s)")
    plt.xlabel("Num Points")
    leg = plt.legend(loc='upper center')
    plt.show()


def find_expected_value(count_arr=[]):
    if len(count_arr) != 0:
        exp_value = np.mean(count_arr)
    else:

        f = open("q4Plots/output2").readlines()
        # print(f)
        arr = []
        for num in f:
            x = num.split('->')
            arr.append(int(x[1]))
            print(int(x[1]))
            arr.append(int(x[1]))
        exp_value = np.mean(arr)

    
    return exp_value



def karat_threshold_exp_2():

    t_exp = defaultdict(list)
    x_axis = []
    time_sum = []
    for threshold in range(1,200):
        x_axis.append(threshold)
        # print(threshold)
        tmp = 0
        cnt = 0
        for i in range(1,50):
            cnt += 1
            print(threshold, i)

            t = run_experiment(30, i, threshold)
            t_exp[i].append(t)
            tmp += t
        time_sum.append(tmp)

    print(time_sum)
    print(time_sum.index(min(time_sum))+1)

    plot_figure(x_axis, y_array2= time_sum, x_label="Threshold", y_axis_label="Time(s)", optional=time_sum.index(min(time_sum))+1)

    return 
    arr = []
    for i in t_exp:

        mini = min(t_exp[i])
        ind = t_exp[i].index(mini)
        print(i, "->", t_exp[i].index(mini))
        arr.append(ind+1)
    exp_value = find_expected_value(arr)
    print(exp_value)
    return


    print(t_exp)

    for i in t_exp:
        plt.plot(x_axis, t_exp[i], label="n = "+str(i))

    plt.title('Title')
    plt.ylabel("Time(s)")
    plt.xlabel("Thresholds")
    leg = plt.legend(loc='upper center')
    plt.show()


# print(karatsuba_with_diff_thresholds())
karat_threshold_exp_2()
# find_expected_value()