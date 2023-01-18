import copy
from state import *

# DFA is a class with four fields:
# -states = a list of states in the DFA
#  Note that the start state is always state 0
# -accepting = A dictionary, the key is the state id 
#  and value is a boolean indicating which states are acceping
# -alphabet = a list of symbols in the alphabet of the regular language.
#  Note that & can not be included because we use it as epsilon
# -startS = it is the start state id which we assume it is always 0
class DFA:
    def __init__(self):
        self.states = []
        self.is_accepting= dict()
        self.alphabet = []
        self.startS = 0
        pass
    def __str__(self):
        pass  
    # You should write this function.
    # It takes two states and a symbol/char. It adds a transition from 
    # the first state of the DFA to the other input state of the DFA.
    def addTransition(self, s1, s2, sym):
        if sym not in self.states[s1.id].transition:
            self.states[s1.id].transition[sym] = set()
        self.states[s1.id].transition[sym].add(s2)
        pass 
    # You should write this function.
    # It returns a DFA that is the complement of this DFA
    def complement(self):
        dfa = DFA()
        dfa.states = self.states
        dfa.alphabet = self.alphabet
        for i in range(len(dfa.states)):
            if i not in self.is_accepting:
                dfa.is_accepting.update({i: True})
        # print(dfa.is_accepting)
        # print(self.is_accepting)
        return dfa
    # You should write this function.
    # It takes a string and returns True if the string is in the language of this DFA

    def isStringInLanguage(self, string):
        queue = [(self.states[0], 0)]
        currS = self.states[0]
        pos = 0
        visited = []
        while queue:
            currS, pos = queue.pop()
            # print(pos, len(string))
            if pos == len(string):
                if currS.id in self.is_accepting and self.is_accepting[currS.id]:
                    return self.is_accepting[currS.id]
                continue
            for s in self.states:
                if s.id == currS.id:
                    if string[pos] in s.transition:
                        stats = s.transition[string[pos]]
                        for stat in stats:
                            queue.extend([(stat,pos+1)])
                    break
        if pos == len(string):
            return currS.id in self.is_accepting and self.is_accepting[currS.id]
        else:
            return False
    # You should write this function.
    # It runs BFS on this DFA and returns the shortest string accepted by it
    def shortestString(self):
        queue = [[self.states[0]]]
        currS = self.states[0]
        visited = []

        if currS.id in self.is_accepting and self.is_accepting[currS.id]:# {0: True}
            return True

        while queue:
            currS = queue.pop(0)
            node  = currS[-1]
            # Condition to check if the
            # current node is not visited
            if node.id not in visited:
                #[('a', {<state.State object at 0x104bb6970>}), ('b', {<state.State object at 0x104bb6940>})]
                neighbours = list(self.states[node.id].transition.items())
                
                # Loop to iterate over the
                # neighbours of the node
                for neighbour in neighbours:
                    new_path = list(currS)

                    for stat in neighbour[1]:
                        new_path.append(stat)
                    queue.append(new_path)
                    
                    # Condition to check if the
                    # neighbour node is the goal
                    if stat.id in self.is_accepting and self.is_accepting[stat.id]:
                        string = ''
                        for s in range(len(new_path)-1):
                            for sym, state in list(self.states[new_path[s].id].transition.items()):
                                for st in state:
                                    if st.id == new_path[s + 1].id:
                                        string = string + str(sym)
                        return string
                visited.append(node.id)
        
        return None