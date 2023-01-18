

import sys
import time
from functools import cache
import matplotlib.pyplot as plt
import random

sys.setrecursionlimit(4000)
def initial(file):
    vault = []
    with open(file, 'r') as f:
        for line in f.readlines():
            line = line.rstrip('\n') 
            vault.append(line.split(','))
    vault = tuple([tuple([int(vault[x][y]) for y in range(len(vault[0]))]) for x in range(len(vault))])
    return vault

# @cache
# def vaultDFSearch(i, j, path, vault):
#         # Base case: all change made no more path need to be added
#     if i < 0 or j < 0:
#         return -1, ""
#     # choose to go west
#     left, leftpath = vaultSearch(i - 1, j, path, vault)
#     # choose to go north
#     right, rightpath = vaultSearch(i, j - 1, path, vault)

#     if i + j != 0:
#         if left > right:
#             path = "N" + leftpath
#         else:
#             path = "W" + rightpath
#     else:
#         left = 0
#         right = 0
#     return max(left, right) + int(vault[i][j]), path

def vaultOut(vault):
    total = tuple([tuple([random.randrange(0, 50) for x in range(len(vault) - 1)]) for y in range(len(vault[0]) - 1)])
    # base case: the last element in total = start
    total[len(vault) - 1][len(vault[0]) - 1] = int(vault[len(vault) - 1][len(vault[0]) - 1])

    # From last row to 0
    for i in range(len(vault)-1, -1, -1):
        # From last column to 0
        for j in range(len(vault[0])-1, -1, -1):
            # except base case
            if i < len(vault)-1 or j < len(vault[0])-1:
                # if at the last row
                if i == len(vault) - 1:
                    total[i][j] = int(vault[i][j]) + total[i][j + 1]
                # if at the last column
                elif j == len(vault[0]) - 1:
                    total[i][j] = int(vault[i][j]) + total[i + 1][j]
                else:
                    total[i][j] = int(vault[i][j]) + max(total[i + 1][j], total[i][j + 1])
    return total

def solution(vault):

    def helper(i, j):
        if i == 0 and j == 0:
            return vault[0][0], ""
        if i > 0 or j > 0:
            # if at the first row
            if i == 0:
                total, path = helper(i, j - 1)
                path = "W" + path
                return  vault[i][j] + total, path
            # if at the first column
            elif j == 0:
                total, path = helper(i - 1, j)
                path = "N" + path
                return vault[i][j]+ total, path
            else:
                total1, path1 = helper(i, j - 1)
                total2, path2 = helper(i - 1, j)
                if total1 >= total2:
                    path = "W" + path1
                    return vault[i][j] + total1, path
                else:
                    path = "N" + path2
                    return vault[i][j] + total2, path
    return helper(len(vault) - 1, len(vault[0]) - 1)


def solutiondp(vault):
    @cache
    def helper(i, j):
        if i == 0 and j == 0:
            return vault[0][0], ""
        if i > 0 or j > 0:
            # if at the first row
            if i == 0:
                total, path = helper(i, j - 1)
                path = "W" + path
                return  vault[i][j] + total, path
            # if at the first column
            elif j == 0:
                total, path = helper(i - 1, j)
                path = "N" + path
                return vault[i][j]+ total, path
            else:
                total1, path1 = helper(i, j - 1)
                total2, path2 = helper(i - 1, j)
                if total1 >= total2:
                    path = "W" + path1
                    return vault[i][j] + total1, path
                else:
                    path = "N" + path2
                    return vault[i][j] + total2, path
    return helper(len(vault) - 1, len(vault[0]) - 1)

def printOut(total, vault, time):
    path = ""
 
    row = len(vault) - 1
    col = len(vault[0]) - 1
    coin = total[0][0]

    value = coin
    xpos = 0
    ypos = 0

    for i in range(0, row + col):
        value = value - int(vault[xpos][ypos])
        if xpos + 1 <= row:
            if value == total[xpos + 1][ypos]:
                path = "N" + path
                xpos = xpos + 1
        if ypos + 1 <= col:
            if value == total[xpos][ypos + 1]:
                path = "W" + path
                ypos = ypos + 1

    print(path, coin, time, sep="\n")

def plotGaph(arrsize, time1, time2):
    plt.figure(figsize=(14, 7))
    plt.plot(arrsize, time1, label='dynamic programming')
    plt.plot(arrsize, time2, label='without dynamic programming')

    plt.xticks(arrsize)
    plt.ylim([0, time1[len(time1) - 1]])
    plt.ticklabel_format(style="plain")
    plt.xlabel('N')
    plt.ylabel('Runtime (ns)')
    plt.title("Runtime of vault")

    plt.legend()
    plt.grid()
    plt.savefig("vault.eps")
    plt.show()

def createTest():
    N = 4
    arrsize = []
    runtime1 = []
    runtime2 = []
    for i in range (0, 12):
        matrix = tuple([tuple([random.randrange(0, 50) for x in range(N)]) for y in range(N)])

        start = time.perf_counter_ns()
        #coins = vaultOut(matrix)
        coins, path = solutiondp(matrix)
        end = time.perf_counter_ns()
        vaulttime1 = float(format(end - start, '.3g'))
        
        start = time.perf_counter_ns()
        coins, path = solution(matrix)
        end = time.perf_counter_ns()
        vaulttime2 = float(format(end - start, '.3g'))

        arrsize.append(N)
        runtime1.append(vaulttime1)
        runtime2.append(vaulttime2)
        N = N + 1

    plotGaph(arrsize,runtime1, runtime2)


if __name__ == "__main__":
    # print(f"Arguments count: {len(sys.argv)}")
    vault = initial(sys.argv[1])
    # # print(vault)
    start = time.perf_counter()
    coins, path = solutiondp(vault)
    end = time.perf_counter()
    print(path, coins, float(format(end - start, '.3g')), sep='\n')

    # createTest()

