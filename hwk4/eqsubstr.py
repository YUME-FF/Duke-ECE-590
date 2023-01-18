# Write a function, which when iven one string (s) and two characters
# (c1 and c2), computes all pairings of contiguous ranges of c1s
# and c2s that have the same length.  Your function should return
# a set of three-tuples.  Each element of the set should be
# (c1 start index, c2 start index, length)
#
# Note that s may contain other characters besides c1 and c2.
# Example:
#  s = abcabbaacabaabbbb
#      01234567890111111  <- indices for ease of looking
#                1123456
#  c1 = a
#  c2 = b
#  Observe that there are the following contiguous ranges of 'a's (c1)
#  Length 1: starting at 0, 3, 9
#  Length 2: starting at 6, 11
#  And the following contiguous ranges of 'b's (c2)
#  Length 1: starting at 1, 10
#  Length 2: starting at 4
#  Length 4: starting at 13
#  So the answer would be
#  { (0, 1, 1), (0, 10, 1), (3, 1, 1), (3, 10, 1), (9, 1, 1), (9, 10, 1),
#    (6, 4, 2), (11, 4, 2)}
#  Note that the length 4 range of 'b's does not appear as there are no
#  Length 4 runs of 'a's.
import random
import time

import numpy as np
import matplotlib.pyplot as plt


def matching_length_sub_strs(s, c1, c2):
    # WRITE ME
    c1Tuple = []
    c2Tuple = []
    length1 = index1 = length2 = index2 = 0
    # make 2 set of 2-tuple (index, length)
    for i in range(0, len(s)):
        if s[i] != c1 or i == len(s)-1:
            if length1 > 0:
                c1Tuple.append((index1, length1))
            length1 = 0
        else:
            length1 = length1 +1
            if length1 == 1:
                index1 = i
        if s[i] != c2 or i == len(s)-1:
            if length2 > 0:
                c2Tuple.append((index2, length2))
            length2 = 0
        else:
            length2 = length2 + 1
            if length2 == 1:
                index2 = i
    # append a set of 3-tuple from the 2 set
    ans = set()
    for i in range(0, len(c1Tuple)):
        for j in range(0, len(c2Tuple)):
            if c1Tuple[i][1] == c2Tuple[j][1]:
                ans.add((c1Tuple[i][0], c2Tuple[j][0], c1Tuple[i][1]))

    return ans


# Makes a random string of length n
# The string is mostly comprised of 'a' and 'b'
# So you should use c1='a' and c2='b' when
# you use this with matching_length_sub_strs
def rndstr(n):
    def rndchr():
        x=random.randrange(7)
        if x==0:
            return chr(random.randrange(26)+ord('A'))
        if x<=3:
            return 'a'
        return 'b'
    ans=[rndchr() for i in range(n)]
    return "".join(ans)

def best(n):
    ans=['a' for i in range(int(n/2))]
    for i in range(int(n/2),n):
        ans.append('b')
    return "".join(ans)

def worst(n):
    ans=['ab' for i in range(int(n/2))]
    if n % 2 == 1:
        ans.append('a')
    return "".join(ans)

def plotGaph(arrsize, arrtime1, arrtime2, arrtime3):
    plt.figure(figsize=(14, 7))
    plt.plot(arrsize, arrtime1, label='Best')
    plt.plot(arrsize, arrtime2, label='Worst')
    plt.plot(arrsize, arrtime3, label='Rndstr')

    plt.xticks(arrsize)
    plt.ticklabel_format(style="plain")
    plt.yticks(np.arange(0, 30, step=5))
    plt.xlabel('size')
    plt.ylabel('Runtime (s)')
    # plt.figure(dpi=600)
    plt.title("Runtime of substr()")

    plt.legend()
    plt.grid()
    plt.savefig("substrs.eps")
    plt.show()

if __name__ == "__main__":
    # s = 'abcabbaacabaabbbb'
    # ans = matching_length_sub_strs(s, 'a','b')
    size = 512
    arrsize = []
    arrtime1 = []
    arrtime2 = []
    arrtime3 = []
    while(size <= 16384):
        start = time.perf_counter()
        ans = matching_length_sub_strs(best(size), 'a', 'b')
        end = time.perf_counter()
        time1 = end - start
        arrtime1.append(time1)
        ans.clear()

        start = time.perf_counter()
        ans = matching_length_sub_strs(worst(size), 'a', 'b')
        end = time.perf_counter()
        time2 = end - start
        arrtime2.append(time2)
        ans.clear()

        start = time.perf_counter()
        ans = matching_length_sub_strs(rndstr(size), 'a', 'b')
        end = time.perf_counter()
        time3 = end - start
        arrtime3.append(time3)
        ans.clear()

        print(size, time1, time2, time3, sep=',')
        arrsize.append(size)
        size = 2 * size
    plotGaph(arrsize, arrtime1, arrtime2, arrtime3)