# removes duplicates from data.
# This function keeps the last occurence of each element
# and preserves order.
# So rmdup([1,2,3,2,1,4,2]) should return [3,1,4,2]
import random
import time
import numpy as np
import matplotlib.pyplot as plt

def rmdup(data):
    # Write me
    ans = {}
    data = data[::-1]
    ans = ans.fromkeys(data)
    ans = list(ans)
    ans = ans[::-1]
    return ans

def exipertment(size):
    arrsize = []
    arrtime1 = []
    arrtime2 = []
    arrtime3 = []
    dataMany = []
    dataModerate = []
    dataRare = []
    for count in range(0, 11):
        for i in range(0, size):
            dataMany.append(random.randrange(0, int(size / 2048)))
            dataModerate.append(random.randrange(0, int(size / 16)))
            dataRare.append(random.randrange(0, size))
        start = time.perf_counter()
        dataMany = rmdup(dataMany)
        end = time.perf_counter()
        time1 = (end - start) * 1000

        start = time.perf_counter()
        dataModerate = rmdup(dataModerate)
        end = time.perf_counter()
        time2 = (end - start) * 1000

        start = time.perf_counter()
        dataRare = rmdup(dataRare)
        end = time.perf_counter()
        time3 = (end - start) * 1000

        print(size, time1, time2, time3, sep=",")
        arrsize.append(size)
        size = 2 * size
        arrtime1.append(time1)
        arrtime2.append(time2)
        arrtime3.append(time3)
        dataMany.clear()
        dataModerate.clear()
        dataRare.clear()
    return arrsize, arrtime1, arrtime2, arrtime3

def plotGaph(arrsize, arrtime1, arrtime2, arrtime3):
    plt.figure(figsize=(14, 7))
    plt.plot(arrsize, arrtime1, label='Many')
    plt.plot(arrsize, arrtime2, label='Moderate')
    plt.plot(arrsize, arrtime3, label='Rare')

    xtick = [arrsize[0], arrsize[len(arrsize)-4], arrsize[len(arrsize)-3], arrsize[len(arrsize)-2], arrsize[len(arrsize)-1]]
    plt.xticks(xtick)
    plt.ticklabel_format(style="plain")
    plt.yticks(np.arange(0, 1200, step=100))
    plt.xlabel('size')
    plt.ylabel('Runtime (ms)')
    # plt.figure(dpi=600)
    plt.title("Runtime of rmdup()")

    plt.legend()
    plt.grid()
    plt.savefig("rmdup.eps")

    plt.show()


if __name__ == "__main__":
    size = 4096
    arrsize, arrtime1, arrtime2, arrtime3 = exipertment(size)
    plotGaph(arrsize, arrtime1, arrtime2, arrtime3)

        
