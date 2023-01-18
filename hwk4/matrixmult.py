# This function takes 2 matricies (as lists of lists)
# and performs matrix multiplication on them.
# Note: you may not use any matrix multiplication libraries.
# You need to do the multiplication yourself.
# For example, if you have
#     a=[[1,2,3],
#        [4,5,6],
#        [7,8,9],
#        [4,0,7]]
#     b=[[1,2],
#        [3,4],
#        [5,6]]
#  Then a has 4 rows and 3 columns.
#  b has 3 rows and 2 columns.
#  Multiplying a * b results in a 4 row, 2 column matrix:
#  [[22, 28],
#   [49, 64],
#   [76, 100],
#   [39, 50]]
import random
import time
import numpy as np
import matplotlib.pyplot as plt

def matrix_mul(a,b):
    # Write me
    ans = []
    for i in range(0, len(a)):
        ans.append([])
        for j in range(0, len(b[0])):
            mutiplyEle = 0
            for k in range(0, len(a[0])):
                mutiplyEle += a[i][k]*b[k][j]
            ans[i].append(mutiplyEle)
    return ans

def plotGaph(arrsize, arrtime1, arrtime2, arrtime3):
    plt.figure(figsize=(14, 7))
    plt.plot(arrsize, arrtime1, label='Many')
    plt.plot(arrsize, arrtime2, label='Square')
    plt.plot(arrsize, arrtime3, label='Fewer')

    xtick = [arrsize[0],arrsize[len(arrsize)-6],arrsize[len(arrsize)-5], arrsize[len(arrsize)-4], arrsize[len(arrsize)-3], arrsize[len(arrsize)-2], arrsize[len(arrsize)-1]]
    plt.xticks(xtick)
    plt.ticklabel_format(style="plain")
    plt.yticks(np.arange(0, 300, step=30))
    plt.xlabel('size')
    plt.ylabel('Runtime (s)')
    # plt.figure(dpi=600)
    plt.title("Runtime of matrix_mul()")

    plt.legend()
    plt.grid()
    plt.savefig("matrixmult.eps")
    plt.show()

if __name__ == "__main__":
    N=4
    arrsize = []
    arrtime1 = []
    arrtime2 = []
    arrtime3 = []
    matManyA = []
    matManyB = []
    matSquA = []
    matSquB = []
    matFewA = []
    matFewB = []
    for count in range(0,8):
        for row in range(0, 4*N):
            matManyA.append([])
            for column in range(0, N):
                matManyA[row].append(random.randrange(0, 10))
        for row in range(0, N):
            matManyB.append([])
            for column in range(0, 4*N):
                matManyB[row].append(random.randrange(0, 10))

        for row in range(0, N):
            matSquA.append([])
            for column in range(0, N):
                matSquA[row].append(random.randrange(0, 10))
        for row in range(0, N):
            matSquB.append([])
            for column in range(0, N):
                matSquB[row].append(random.randrange(0, 512))

        for row in range(0, int(N/4)):
            matFewA.append([])
            for column in range(0, N):
                matFewA[row].append(random.randrange(0, 512))
        for row in range(0, N):
            matFewB.append([])
            for column in range(0, int(N/4)):
                matFewB[row].append(random.randrange(0, 512))

        start = time.perf_counter()
        dataMany = matrix_mul(matManyA, matManyB)
        end = time.perf_counter()
        time1 = end - start

        start = time.perf_counter()
        dataSqu = matrix_mul(matSquA, matSquB)
        end = time.perf_counter()
        time2 = end - start

        start = time.perf_counter()
        dataFew = matrix_mul(matFewA, matFewB)
        end = time.perf_counter()
        time3 = end - start
        print(N, time1, time2, time3, sep=",")
        N = 2 * N
        arrsize.append(N)
        arrtime1.append(time1)
        arrtime2.append(time2)
        arrtime3.append(time3)
        matManyA.clear()
        matManyB.clear()
        matSquA.clear()
        matSquB.clear()
        matFewA.clear()
        matFewB.clear()

    # plotGaph(arrsize, arrtime1, arrtime2, arrtime3)