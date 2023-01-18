import sys
import time
from functools import cache
import matplotlib.pyplot as plt
import random

sys.setrecursionlimit(4000)
def initial(file):
    mat = []
    with open(file, 'r') as f:
        for line in f.readlines():
            line = line.rstrip('\n') 
            mat.append(line.split(','))
    
    mat.insert(0,[mat[0][0],0,mat[0][1]])
    mat = tuple([tuple([mat[x][y] for y in range(len(mat[0]))]) for x in range(len(mat))])
    return mat


def solution(mat):

    def helper(i,j):
        if i == j:
            return 0, mat[j][0]

        _min = sys.maxsize

        for k in range(i, j):
            count1, path1 = helper(i, k)
            count2, path2 = helper(k + 1, j)
            count = (count1+ count2
                + int(mat[i-1][2])*int(mat[k][2])*int(mat[j][2]))

            if count < _min:
                _min = count
                outpath1 = path1
                outpath2 = path2
 
        # Return minimum count
        return _min, (outpath1, outpath2)
    return helper(1, len(mat) - 1)


def solutiondp(mat):
    @cache
    def helper(i,j):
        if i == j:
            return 0, mat[j][0]

        _min = sys.maxsize

        for k in range(i, j):
            count1, path1 = helper(i, k)
            count2, path2 = helper(k + 1, j)
            count = (count1+ count2
                + int(mat[i-1][2])*int(mat[k][2])*int(mat[j][2]))

            if count < _min:
                _min = count
                outpath1 = path1
                outpath2 = path2
 
        # Return minimum count
        return _min, (outpath1, outpath2)
    return helper(1, len(mat) - 1)


def plotGaph(arrsize, time1, time2):
    plt.figure(figsize=(14, 7))
    plt.plot(arrsize, time1, label='dynamic programming')
    plt.plot(arrsize, time2, label='without dynamic programming')

    plt.xticks(arrsize)
    plt.ylim([0, time1[len(time1) - 1]])
    plt.ticklabel_format(style="plain")
    plt.xlabel('N')
    plt.ylabel('Runtime (ns)')
    plt.title("Runtime of mat")

    plt.legend()
    plt.grid()
    plt.savefig("mat.eps")
    plt.show()

def createTest():
    N = 4
    arrsize = []
    runtime1 = []
    runtime2 = []
    for i in range (0, 13):
        matrix = [[y, random.randrange(1, 100), 0] for y in range(N)]
        matrix[0][2] = 10
        for x in range(1, N):
            matrix[x][2] = matrix[x][1]
            matrix[x][1] = matrix[x-1][2]

        mat = tuple([tuple([matrix[x][y] for y in range(len(matrix[0]))]) for x in range(len(matrix))])

        start = time.perf_counter_ns()
        coins, path = solutiondp(mat)
        end = time.perf_counter_ns()
        vaulttime1 = float(format(end - start, '.3g'))
        print(coins, float(format(end - start, '.3g')))
        start = time.perf_counter_ns()
        coins, path = solution(mat)
        end = time.perf_counter_ns()
        vaulttime2 = float(format(end - start, '.3g'))
        print(coins, float(format(end - start, '.3g')))

        arrsize.append(N)
        runtime1.append(vaulttime1)
        runtime2.append(vaulttime2)
        N = N + 1
        print(N)

    plotGaph(arrsize,runtime1, runtime2)

if __name__ == "__main__":
    # print(f"Arguments count: {len(sys.argv)}")
    mat = initial(sys.argv[1])
    # # print(len(mat) - 1)
    start = time.perf_counter_ns()
    count, path1 = solutiondp(mat)
    end = time.perf_counter_ns()
    print(path1, count, float(format(end - start, '.3g')), sep='\n')
    # createTest()