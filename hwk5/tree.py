import time
import sys
from functools import cache
import matplotlib.pyplot as plt
import random

class TreeNode:
    def __init__(self, val, freq, left, right):
        self.val=val
        self.freq=freq
        self.left=left
        self.right=right
        self.cost = None
        pass
    def __str__(self):
        if self.left is None and self.right is None:
            return str(self.val)
        left = str(self.left) if self.left is not None else '()'
        right = str(self.right) if self.right is not None else '()'
        return '({} {} {})'.format(self.val,left,right)
        
    def computeCost(self):
        if self.cost is not None:
            return self.cost
        def helper(n,depth):
            if n is None:
                return 0
            return depth * n.freq + helper(n.left, depth+1) + helper(n.right, depth +1)
        self.cost = helper(self, 1)
        return self.cost
    pass
pass

# Your code here.
def initial(file):
    tree = []
    with open(file, 'r') as f:
        for line in f.readlines():
            line = line.rstrip('\n') 
            tree.append(line.split(':'))
    tree = tuple([tuple([int(tree[x][y]) for y in range(len(tree[0]))]) for x in range(len(tree))])
    return tree

def insert(root, key):
    if root is None:
        return TreeNode(key[0], key[1], None, None)
    else:
        if root.val == key[0]:
            return root
        elif root.val < key[0]:
            root.right = insert(root.right, key)
        else:
            root.left = insert(root.left, key)
    return root

def build_OBST(data):
    root = None
    # @cache
    def helper(i ,j):
        # Base cases
        if j < i:     # no elements
            return 0, None
        if j == i:     # one element
            return data[i][1], insert(root, data[i])
        
        # Get sum
        fsum = Sum(data, i, j)
        
        # Initialize minimum value
        _min = sys.maxsize

        for r in range(i, j + 1):
            count1, tree1 = helper(i, r - 1)
            count2, tree2 = helper(r + 1, j)
            count = count1+ count2

            if count < _min:
                _min = count
                rootout = TreeNode(data[r][0], data[r][1], None, None)
                rootout.left = tree1
                rootout.right = tree2
            
        # Return minimum value
        return _min + fsum, rootout

    return helper(0, len(data) - 1)

def build_OBSTdp(data):
    root = None
    @cache
    def helper(i ,j):
        # Base cases
        if j < i:     # no elements
            return 0, None
        if j == i:     # one element
            return data[i][1], insert(root, data[i])
        
        # Get sum
        fsum = Sum(data, i, j)
        
        # Initialize minimum value
        _min = sys.maxsize

        for r in range(i, j + 1):
            count1, tree1 = helper(i, r - 1)
            count2, tree2 = helper(r + 1, j)
            count = count1+ count2

            if count < _min:
                _min = count
                rootout = TreeNode(data[r][0], data[r][1], None, None)
                rootout.left = tree1
                rootout.right = tree2
            
        # Return minimum value
        return _min + fsum, rootout

    return helper(0, len(data) - 1)

def Sum(data, i, j):
    s = 0
    for k in range(i, j + 1):
        s += data[k][1]
    return s

def plotGaph(arrsize, time1, time2):
    plt.figure(figsize=(14, 7))
    plt.plot(arrsize, time1, label='dynamic programming')
    plt.plot(arrsize, time2, label='without dynamic programming')

    plt.xticks(arrsize)
    plt.ylim([0, time1[len(time1) - 1]])
    plt.ticklabel_format(style="plain")
    plt.xlabel('Number of Nodes')
    plt.ylabel('Runtime (ns)')
    plt.title("Runtime of tree")

    plt.legend()
    plt.grid()
    plt.savefig("tree.eps")
    plt.show()

def createTest():
    N = 4
    arrsize = []
    runtime1 = []
    runtime2 = []
    for i in range (0, 13):
        mat = tuple([tuple([random.randrange(1, 100), random.randrange(1, 10)]) for x in range(N)])

        start = time.perf_counter_ns()
        count, path = build_OBSTdp(mat)
        end = time.perf_counter_ns()
        vaulttime1 = float(format(end - start, '.3g'))
        print(count, float(format(end - start, '.3g')))

        start = time.perf_counter_ns()
        count, path = build_OBST(mat)
        end = time.perf_counter_ns()
        vaulttime2 = float(format(end - start, '.3g'))
        print(count, float(format(end - start, '.3g')))

        arrsize.append(N)
        runtime1.append(vaulttime1)
        runtime2.append(vaulttime2)
        N = N + 1
        print(N)

    plotGaph(arrsize,runtime1, runtime2)


if __name__=="__main__":
     data = initial(sys.argv[1])   
     start = time.perf_counter_ns()  
     count, tree = build_OBSTdp(data)
     end = time.perf_counter_ns()
     print(tree, count, float(format(end - start, '.3g')), sep='\n')
    # createTest()