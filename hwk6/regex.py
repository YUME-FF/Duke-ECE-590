from nfa import *
from state import *

class Regex:
    def __repr__(self):
        ans=str(type(self))+"("
        sep=""
        for i in self.children:
            ans = ans + sep + repr(i)
            sep=", "
            pass
        ans=ans+")"
        return ans
    def transformToNFA(self):
        pass
    pass

class ConcatRegex(Regex):
    def __init__(self, r1, r2):
        self.children=[r1,r2]
        pass
    def __str__(self):
        return "{}{}".format(self.children[0],self.children[1])
    def transformToNFA(self):
        nfa1 = self.children[0].transformToNFA()
        length1 = len(nfa1.states)

        nfa2 = self.children[1].transformToNFA()
        length2 = len(nfa2.states)
        
        nfa1.addStatesFrom(nfa2)
        nfa1.accepting = {}

        for acc in nfa2.accepting:
            nfa1.accepting.update({acc + length1: nfa2.accepting[acc]})

        nfa1.alphabet = nfa1.alphabet + nfa2.alphabet
        return nfa1
    pass

class StarRegex(Regex):
    def __init__(self, r1):
        self.children=[r1]
        pass
    def __str__(self):
        return "({})*".format(self.children[0])
    def transformToNFA(self):
        nfa = self.children[0].transformToNFA()

        n = NFA()
        n.alphabet = nfa.alphabet
        n.states.append(State(0))
        n.addStatesFrom(nfa)
        
        n.states.append(State(len(n.states)))
        n.addTransition(n.states[0], n.states[len(n.states) - 1])

        for acc in nfa.accepting:
            if acc != 0:
                n.addTransition(n.states[acc + 1], n.states[1])
            n.addTransition(n.states[acc + 1], n.states[len(n.states) - 1])
        
        n.accepting.update({len(n.states) - 1: True})
        return n

        # nfa.accepting.update({0: True})
        # for acc in nfa.accepting:
        #     if acc != 0:
        #         nfa.addTransition(nfa.states[acc], nfa.states[0])
        
        # return nfa
    pass

class OrRegex(Regex):
    def __init__(self, r1, r2):
        self.children=[r1,r2]
        pass
    def __str__(self):
        return "(({})|({}))".format(self.children[0],self.children[1])
    def transformToNFA(self):
        nfa1 = self.children[0].transformToNFA()
        length1 = len(nfa1.states)
        
        nfa2 = self.children[1].transformToNFA()
        length2 = len(nfa2.states)

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

class SymRegex(Regex):
    def __init__(self, sym):
        self.sym=sym
        pass
    def __str__(self):
        return self.sym
    def __repr__(self):
        return self.sym
    def transformToNFA(self):
        n = NFA()
        n.states.append(State(0))
        n.states.append(State(1))
        n.addTransition(State(0), State(1), str(self))
        n.accepting = {n.states[1].id: True}
        n.alphabet.append(self.sym)
        return n
    pass

class EpsilonRegex(Regex):
    def __init__(self):
        pass
    def __str__(self):
        return '&'
    def __repr__(self):
        return '&'
    def transformToNFA(self):
        n = NFA()
        n.states.append(State(0))
        n.accepting = {n.states[0].id: True}
        return n
    pass

class ReInput:
    def __init__(self,s):
        self.str=s
        self.pos=0
        pass
    def peek(self):
        if (self.pos < len(self.str)):
            return self.str[self.pos]
        return None
    def get(self):
        ans = self.peek()
        self.pos +=1
        return ans
    def eat(self,c):
        ans = self.get()
        if (ans != c):
            raise ValueError("Expected " + str(c) + " but found " + str(ans)+
                             " at position " + str(self.pos-1) + " of  " + self.str)
        return c
    def unget(self):
        if (self.pos > 0):
            self.pos -=1
            pass
        pass
    pass

# R -> C rtail
# rtail -> OR C rtail | eps
# C -> S ctail
# ctail -> S ctail | eps
# S -> atom stars
# atom -> (R) | sym | &
# stars -> * stars | eps


#It gets a regular expression string and returns a Regex object. 
def parse_re(s):
    inp=ReInput(s)
    def parseR():
        return rtail(parseC())
    def parseC():
        return ctail(parseS())
    def parseS():
        return stars(parseA())
    def parseA():
        c=inp.get()
        if c == '(':
            ans=parseR()
            inp.eat(')')
            return ans
        if c == '&':
            return EpsilonRegex()
        if c in ')|*':
            inp.unget()
            inp.fail("Expected open paren, symbol, or epsilon")
            pass
        return SymRegex(c)
    def rtail(lhs):
        if (inp.peek()=='|'):
            inp.get()
            x = parseC()
            return rtail(OrRegex(lhs,x))
        return lhs
    def ctail(lhs):
        if(inp.peek() is not None and inp.peek() not in '|*)'):
            temp=parseS()
            return ctail(ConcatRegex(lhs,temp))
        return lhs
    def stars(lhs):
        while(inp.peek()=='*'):
            inp.eat('*')
            lhs=StarRegex(lhs)
            pass
        return lhs
    return parseR()