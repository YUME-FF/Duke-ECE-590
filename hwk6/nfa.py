from state import *
import regex
import copy


# NFA is a class with four fields:
# -states = a list of states in the NFA
#  Note that the start state is always state 0
# -accepting = A dictionary, the key is the state id 
#  and value is a boolean indicating which states are acceping
# -alphabet = a list of symbols in the alphabet of the regular language.
#  Note that & can not be included because we use it as epsilon
# -startS = it is the start state id which we assume it is always 0
class NFA:
    def __init__(self):
        self.states = []
        self.accepting = dict()
        self.alphabet = []
        self.startS = 0
        pass
    def __str__(self):
        pass
    # You should write this function.
    # It takes two states and a symbol. It adds a transition from 
    # the first state of the NFA to the other input state of the NFA.
    def addTransition(self, s1, s2, sym = '&'):
        # self.states[s1.id].transition.update({sym: {s2}})
        if sym not in self.states[s1.id].transition:
            self.states[s1.id].transition[sym] = set()
        self.states[s1.id].transition[sym].add(s2)
        pass
    # You should write this function.
    # It takes an nfa, adds all the states from that nfa and return a 
    # mapping of (state number in old NFA to state number in this NFA) as a dictionary.
    def addStatesFrom(self, nfa):
        n = len(self.states)
        for s in nfa.states:
            k = s.id + n
            self.states.append(State(k))

        self.addTransition(self.states[n - 1], self.states[n])

        for state in nfa.states:
            for key, stats in nfa.states[state.id].transition.items():
                for s in stats:
                    self.addTransition(self.states[n + state.id], self.states[n + s.id], key)
        
        for acc in self.accepting:
                self.addTransition(self.states[acc], self.states[n])

        # tran_Len = len(nfa.states) - 1
        # for tran in range(tran_Len):
        #     for key, stats in self.states[n + tran].transition.items():
        #         self.addTransition(self.states[n + tran], self.states[n + tran + 1], key)
        pass

    # You should write this function.
    # It takes a state and returns the epsilon closure of that state 
    # which is a set of states which are reachable from this state 
    #on epsilon transitions.
    def epsilonClose(self, ns):
        nss = ns
        states = []
        for n in ns:
            for sym, nn in self.states[n.id].transition.items():
                if sym == '&':
                    for s in nn:
                        # if s not in nss:
                        #     nss.append(s)
                        states.append(s)
        # if nss != ns:
        #     return self.epsilonClose(nss)
        # else:
        #     return nss
        return states
    # It takes a string and returns True if the string is in the language of this NFA
    def isStringInLanguage(self, string):
        queue = [(self.states[0], 0)]
        currS = self.states[0]
        pos = 0
        visited = []
        while queue:
            currS, pos = queue.pop(0)
            if pos == len(string):
                if currS.id in self.accepting and self.accepting[currS.id]:
                    return self.accepting[currS.id]
                for n in self.epsilonClose([currS]):
                    queue.append((n, pos))
                continue
            for s in self.states:
                if s.id == currS.id:
                    if string[pos] in s.transition:
                        stats = s.transition[string[pos]]
                        for stat in stats:
                            queue.extend([(stat,pos+1)])
                            queue.extend([(s,pos+1) for s in self.epsilonClose([stat])])
                    else:
                        for n in self.epsilonClose([currS]):
                            queue.append((n, pos))
                    break
        if pos == len(string):
            return currS.id in self.accepting and self.accepting[currS.id]
        else:
            return False
    def union(self, nfa2):
        nfa1 = NFA()
        nfa1.states.append(State(0))
        nfa1.addStatesFrom(self)

        for key, stats in self.accepting.items():
            nfa1.accepting.update({key + 1: stats})

        length1 = len(nfa1.states)
        for s in nfa2.states:
            k = s.id + length1
            nfa1.states.append(State(k))

        nfa1.addTransition(nfa1.states[0], nfa1.states[length1])

        for state in nfa2.states:
            for key, stats in nfa2.states[state.id].transition.items():
                for s in stats:
                    nfa1.addTransition(nfa1.states[length1 + state.id], nfa1.states[length1 + s.id], key)

        for alph in nfa2.alphabet:
            nfa1.alphabet.append(alph)
        
        for key, stats in nfa2.accepting.items():
            nfa1.accepting.update({key + length1: stats})
        return nfa1
    pass