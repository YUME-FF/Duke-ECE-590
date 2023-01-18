import copy
from state import * 
from regex import *
from nfa import *
from dfa import *
import gc

# You should write this function.
# It takes an NFA and returns a DFA.
def nfaToDFA(nfa):
    dfa = DFA()
    dfa.alphabet = nfa.alphabet
    dfa.states.append(State(0))

    nfa_transition_dict = {}
    dfa_transition_dict = {}

    # Combine NFA transitions
    empty = 0
    for nfa_status in nfa.states: # {(start, sym): end}
        for key, states in nfa.states[nfa_status.id].transition.items():
            for s in states:
                if key == '&':
                    empty = empty + 1
                if (nfa_status.id, key) in nfa_transition_dict:
                    nfa_transition_dict[(nfa_status.id, key)].append(s.id)
                else:
                    nfa_transition_dict[(nfa_status.id, key)] = [s.id]

    # delete empty:
    #a|bc {(0, 'a'): [1], (0, '&'): [2], (2, 'b'): [3], (3, '&'): [4], (4, 'c'): [5]} 
    #->   {(0, 'a'): [1], (0, '&'): [], (0, 'b'): [3], (3, '&'): [4], (4, 'c'): [5]} empty--
    #->   {(0, 'a'): [1], (0, '&'): [], (0, 'b'): [2], (2, '&'): [3], (3, 'c'): [4]}
    #->   {(0, 'a'): [1], (0, '&'): [], (0, 'b'): [2], (2, '&'): [], (2, 'c'): [4]} empty--
    #->   {(0, 'a'): [1], (0, '&'): [], (0, 'b'): [2], (2, '&'): [], (2, 'c'): [3]}
    def delete_empty_helper(transition_dict, accepting):
        start = 0
        dest = 0
        length = 0
        tmp = ()
        minn = len(transition_dict)
        for key, end in list(transition_dict.items()):
            if key[1] == '&':
                countMin = 65536
                count = 0
                for endelement in end:
                    for k, e in list(transition_dict.items()):
                        count = count + e.count(endelement)
                    if countMin > count:
                        countMin = count
                        tmp = key
                        dest = endelement

                # if len(end) > 0:
                #     # print(end)
                #     if len(end) > length:
                #         if minn > min(end):
                #             length = len(end)
                #             tmp = key
                #             minn = min(end)
                #     elif len(end) == length:
                #         if minn > min(end):
                #             length = len(end)
                #             tmp = key
                #             minn = min(end)
        start = tmp[0]
        # dest = min(transition_dict[(tmp)])
        transition_dict[(tmp)].remove(dest)
        for key, end in list(accepting.items()):
            if start < dest:
                if key > dest:
                    accepting[key - 1] = accepting.pop(key)
                elif key == dest:
                    accepting[start] = accepting.pop(key)
            elif start > dest:
                if key > start:
                    accepting[key - 1] = accepting.pop(key)
                elif key == start:
                    accepting[dest] = accepting.pop(key)
        for key, end in list(transition_dict.items()):
            ifnotin = 0
            if start < dest: # s1->&->s2->a->s3 --> s1->a->s2
                if key[0] > dest: #(0, '&'): [2], (3, b): [1, 4] -> (2, b): [1, 3]
                    if (key[0] - 1, key[1]) not in transition_dict:
                        transition_dict[(key[0] - 1, key[1])] = transition_dict.pop((key))
                        ifnotin = 1
                    else:
                        del transition_dict[(key)]
                    for endtmp in range(len(end)): # update destination
                        if end[endtmp] > dest:
                            end[endtmp] = end[endtmp] - 1
                        elif end[endtmp] == dest and start < end[endtmp]:
                            end[endtmp] = start
                    if ifnotin == 1:
                        transition_dict.update({(key[0] - 1, key[1]): end})
                    else:
                        for e in end:
                            transition_dict[(key[0] - 1, key[1])].append(e)
                elif key[0] == dest: #(0, '&'): [2], (2, b): [3] -> (0, b): [2]
                    if (start, key[1]) not in transition_dict:
                        transition_dict[(start, key[1])] = transition_dict.pop((key))
                        ifnotin = 1
                    else:
                        del transition_dict[(key)]
                    for endtmp in range(len(end)):
                        if end[endtmp] > dest:
                            end[endtmp] = end[endtmp] - 1
                        elif end[endtmp] == dest:
                            end[endtmp] = start
                    if ifnotin == 1:
                        transition_dict.update({(start, key[1]): end})
                    else:
                        for e in end:
                            transition_dict[(start, key[1])].append(e)
                else: # key[0] < dest and start < dest
                    #(0, '&'): [2], (1, b): [3] -> (1, b): [2] start<key[0]<dest
                    #(2, '&'): [4], (1, b): [3, 5] -> (1, b): [3， 4]  key[0]<start<dest
                    #(2, '&'): [4], (1, b): [3, 4] -> (1, b): [3， 2]  key[0]<start<dest
                    #(2, '&'): [4], (2, b): [3, 5] -> (2, b): [3， 4]  key[0] = start
                    for endtmp in range(len(end)):
                        if end[endtmp] > dest:
                            end[endtmp] = end[endtmp] - 1
                        elif end[endtmp] == dest:
                            end[endtmp] = start
                    transition_dict.update({(key): end})
            elif start > dest:# s1->a->s2->&->s1 --> s1->a->s1
                if key[0] > start: #(2, '&'): [0], (3, b): [1, 4] -> (2, b): [0, 3]
                    if (key[0] - 1, key[1]) not in transition_dict:
                        transition_dict[(key[0] - 1, key[1])] = transition_dict.pop((key))
                        ifnotin = 1
                    else:
                        del transition_dict[(key)]
                    for endtmp in range(len(end)): # update destination
                        if end[endtmp] > start:
                            end[endtmp] = end[endtmp] - 1
                        elif end[endtmp] == start and dest < end[endtmp]:
                            end[endtmp] = dest
                    if ifnotin == 1:
                        transition_dict.update({(key[0] - 1, key[1]): end})
                    else:
                        for e in end:
                            transition_dict[(key[0] - 1, key[1])].append(e)
                elif key[0] == start: #(2, '&'): [0], (0, b): [3] -> (1, b): [2]
                    if (dest, key[1]) not in transition_dict:
                        transition_dict[(dest, key[1])] = transition_dict.pop((key))
                        ifnotin = 1
                    else:
                        del transition_dict[(key)]
                    for endtmp in range(len(end)):
                        if end[endtmp] > start:
                            end[endtmp] = end[endtmp] - 1
                        elif end[endtmp] == start:
                            end[endtmp] = dest
                    if ifnotin == 1:
                        transition_dict.update({(dest, key[1]): end})
                    else:
                        for e in end:
                            transition_dict[(dest, key[1])].append(e)
                else: # key[0] < dest and start > dest
                    #(2, '&'): [0], (1, b): [3] -> (1, b): [2]
                    #(4, '&'): [2], (1, b): [3, 5] -> (1, b): [2， 4]
                    #(4, '&'): [2], (1, b): [3, 2] -> (1, b): [2， 3]
                    for endtmp in range(len(end)):
                        if end[endtmp] > start:
                            end[endtmp] = end[endtmp] - 1
                        elif end[endtmp] == start:
                            end[endtmp] = dest
                    transition_dict.update({(key): end})

        return transition_dict, accepting
        
    # Convert NFA transitions to DFA transitions
    dfa_transition_dict = nfa_transition_dict
    # delete empty
    dfa_accepting = nfa.accepting
    # print(dfa_transition_dict)
    # print(nfa.accepting)

    while(empty > 0):
        for key, end in list(dfa_transition_dict.items()):
            orglen = len(end)
            end = list(set(end))
            aftlen = len(end)
            empty = empty + aftlen - orglen
            dfa_transition_dict.update({(key): end})
        # print(dfa_transition_dict)
        # print(dfa_accepting)
        dfa_transition_dict, dfa_accepting = delete_empty_helper(dfa_transition_dict, dfa_accepting)
        empty = empty - 1
    # print(dfa_transition_dict)
    # print(dfa_accepting)
    for key, end in list(dfa_transition_dict.items()):
        if key[1] == '&':
            del dfa_transition_dict[(key)]
    # build DFA transition state pair: {((start states), sym): [dest states]}
    # print(dfa_transition_dict)

    def tran_helper():
        transition_dict = {}
        state = []
        state.append((0,))
        # Convert NFA transitions to DFA transitions
        for dfa_state in state:
            for symbol in dfa.alphabet:
                if len(dfa_state) == 1 and (dfa_state[0], symbol) in dfa_transition_dict:
                    transition_dict[(dfa_state, symbol)] = dfa_transition_dict[(dfa_state[0], symbol)]
                    
                    if tuple(transition_dict[(dfa_state, symbol)]) not in state:
                        state.append(tuple(transition_dict[(dfa_state, symbol)]))
                else:
                    dest = []
                    dest2 = []
                    
                    for nfa_state in dfa_state:
                        if (nfa_state, symbol) in dfa_transition_dict and dfa_transition_dict[(nfa_state, symbol)] not in dest:
                            dest.append(dfa_transition_dict[(nfa_state, symbol)])
                    
                    if not dest:
                        dest2.append(None)
                    else:  
                        for destination in dest:
                            for value in destination:
                                if value not in dest2:
                                    dest2.append(value)
                        
                    transition_dict[(dfa_state, symbol)] = dest2
                        
                    if tuple(dest2) not in state:
                        state.append(tuple(dest2))
        return transition_dict, state
    
    transition_dict, trans = tran_helper()
    # print(transition_dict)

    empty = 0
    #Add transitions
    for key in transition_dict:
        if trans.index(tuple(transition_dict[key])) == len(dfa.states):
            dfa.states.append(State(trans.index(tuple(transition_dict[key]))))
            if empty == 0 and transition_dict[key] == [None]:
                empty = trans.index(tuple(transition_dict[key]))
        dfa.addTransition(dfa.states[trans.index(tuple(key[0]))], dfa.states[trans.index(tuple(transition_dict[key]))], key[1])

    for q_state in trans:
            for nfa_accepting_state in dfa_accepting:
                if nfa_accepting_state in q_state:
                    dfa.is_accepting.update({trans.index(q_state):True})

    # for s in dfa.states:
    #     for key, st in dfa.states[s.id].transition.items():
    #         for ss in st:
    #             print(key, s.id, ss.id)
    # print(dfa.is_accepting)

    return dfa

# You should write this function.
# It takes an DFA and returns a NFA.
def dfaToNFA(dfa):
    nfa = NFA()
    nfa.states = dfa.states
    nfa.accepting = dfa.is_accepting
    nfa.alphabet = dfa.alphabet
    return nfa

# You should write this function.
# It takes two regular expressions and returns a 
# boolean indicating if they are equivalent
def equivalent(re1, re2):
    nfa1 = re1.transformToNFA()
    nfa2 = re2.transformToNFA()
    if nfa1.alphabet != nfa2.alphabet:
        return False

    dfa1 = nfaToDFA(nfa1)
    dfa2 = nfaToDFA(nfa2)

    nfa1_complement = dfaToNFA(dfa1.complement())
    nfa2_complement = dfaToNFA(dfa2.complement())

    union1 = nfa1_complement.union(dfaToNFA(dfa2))
    union2 = nfa2_complement.union(dfaToNFA(dfa1))

    union1_complement = dfaToNFA(nfaToDFA(union1).complement())
    union2_complement = dfaToNFA(nfaToDFA(union2).complement())

    shortestString1 = nfaToDFA(union1_complement).shortestString()
    shortestString2 = nfaToDFA(union2_complement).shortestString()

    # print(shortestString1, shortestString2)
    if shortestString1 == None and shortestString2 == None:
        return True
    else:
        return False

def statehelper(fa):
        for s in fa.states:
            for key, st in fa.states[s.id].transition.items():
                for ss in st:
                    print(s.id, "->", key, "->", ss.id)

if __name__ == "__main__":
    def testNFA(strRe, s, expected):
        re = parse_re(strRe)
        # test your nfa conversion
        nfa = re.transformToNFA()
        res = nfa.isStringInLanguage(s)
        if res == expected:
            print("NFA: ", strRe, " gave ",res, " as expected on ", s)
        else:
            print("**** ", strRe, " Gave ", res , " on " , s , " but expected " , expected)
            pass
        pass

    def testDFA(strRe, s, expected):
        # test your dfa conversion
        re = parse_re(strRe)
        nfa = re.transformToNFA()

        dfa = nfaToDFA(nfa)

        res = dfa.isStringInLanguage(s)
        if res == expected:
            print("DFA: ",strRe, " gave ",res, " as expected on ", s)
        else:
            print("**** DFA: ", strRe, " Gave ", res , " on " , s , " but expected " , expected)
            pass
        pass

    def testEquivalence(strRe1, strRe2, expected):
        re1 = parse_re(strRe1)
        re2 = parse_re(strRe2)
        
        res = equivalent(re1, re2)
        if res == expected:
            print("Equivalence(", strRe1, ", ",strRe2, ") = ", res, " as expected.")
        else:
            print("Equivalence(", strRe1, ", ",strRe2, ") = ", res, " but expected " , expected)
            pass
        pass

    def pp(r):
        print()
        print("Starting on " +str(r))
        re=parse_re(r)
        print(repr(re))
        print(str(re))
        pass
    
    def test():
        testNFA('&','', True)
        testNFA('a', '', False)
        testNFA('a', 'a', True)
        testNFA('a', 'ab', False)
        testNFA('a*', '', True)
        testNFA('a*', 'a', True)
        testNFA('a*', 'aaa', True)
        testNFA('ab', 'ab', True)
        testNFA('ab', 'b', False)
        testNFA('ab', 'a', False)
        testNFA('a|b', '', False)
        testNFA('a|b', 'a', True)
        testNFA('a|b', 'b', True)
        testNFA('a|b', 'ab', False)
        testNFA('ab|cd', '', False)
        testNFA('ab|cd', 'cd', True)
        testNFA('ab|cd*', '', False)
        testNFA('ab|cd*', 'c', True)
        testNFA('ab|cd*', 'cd', True)
        testNFA('ab|cd*', 'cddddddd', True)
        testNFA('ab|cd*', 'ab', True)
        testNFA('(ab)*', 'ababab', True)
        testNFA('((ab)|(cd))*', '', True)
        testNFA('((ab)|(cd))*', 'ab', True)
        testNFA('((ab)|(cd))*', 'cd', True)
        testNFA('((ab)|(cd))*', 'abab', True)
        testNFA('((ab)|(cd))*', 'abcd', True)
        testNFA('((ab)|(cd))*', 'cdcdabcd', True)
        testNFA('((ab|cd)*|e)*', 'cdcdabcd', True) 
        testNFA('((ab|cd)*|(de*fg|h(ij)*klm*n|q))*', '', True)
        testNFA('((ab|cd)*|(de*fg|h(ij)*klm*n|q))*', 'ab', True)
        testNFA('((ab|cd)*|(de*fg|h(ij)*klm*n|q))*', 'abcd', True)
        testNFA('((ab|cd)*|(de*fg|h(ij)*klm*n|q))*', 'cd', True)
        testNFA('((ab|cd)*|(de*fg|h(ij)*klm*n|q))*', 'dfgab', True)
        testNFA('((ab|cd)*|(de*fg|h(ij)*klm*n|q))*', 'defg', True)
        testNFA('((ab|cd)*|(de*fg|h(ij)*klm*n|q))*', 'deeefg', True)
        testNFA('((ab|cd)*|(de*fg|h(ij)*klm*n|q))*', 'hkln', True)
        testNFA('((ab|cd)*|(de*fg|h(ij)*klm*n|q))*', 'q', True)
        testNFA('((ab|cd)*|(de*fg|h(ij)*klm*n|q))*', 'hijijkln', True)
        testNFA('((ab|cd)*|(de*fg|h(ij)*klm*n|q))*', 'hijijklmmmmmmmmmmn', True)
        testNFA('a*b', 'aaab', True)
        testNFA('ba*', 'baaa', True)
        print("")
        print("---------------------------------------")

        testDFA('&','', True)
        testDFA('a', '', False)
        testDFA('a', 'a', True)
        testDFA('a', 'ab', False)
        testDFA('a*', '', True)
        testDFA('a*', 'a', True)
        testDFA('a*', 'aaa', True)
        testDFA('ab', 'ab', True)
        testDFA('ab', 'b', False)
        testDFA('ab', 'a', False)
        testDFA('a|b', '', False)
        testDFA('a|b', 'a', True)
        testDFA('a|b', 'b', True)
        testDFA('a|b', 'ab', False)
        testDFA('ab|cd', '', False)
        testDFA('ab|cd', 'cd', True)
        testDFA('ab|cd*', '', False)
        testDFA('ab|cd*', 'c', True)
        testDFA('ab|cd*', 'cd', True)
        testDFA('ab|cd*', 'cddddddd', True)
        testDFA('ab|cd*', 'ab', True)
        testDFA('(ab)*', 'ababab', True)
        testDFA('((ab)|(cd))*', '', True)
        testDFA('((ab)|(cd))*', 'ab', True)
        testDFA('((ab)|(cd))*', 'cd', True)
        testDFA('((ab)|(cd))*', 'abab', True)
        testDFA('((ab)|(cd))*', 'abcd', True)
        testDFA('((ab)|(cd))*', 'cdcdabcd', True)
        testDFA('((ab|cd)*|e)*', 'cdcdabcd', True) 
        testDFA('((ab|cd)*|(de*fg|h(ij)*klm*n|q))*', '', True)
        testDFA('((ab|cd)*|(de*fg|h(ij)*klm*n|q))*', 'ab', True)
        testDFA('((ab|cd)*|(de*fg|h(ij)*klm*n|q))*', 'abcd', True)
        testDFA('((ab|cd)*|(de*fg|h(ij)*klm*n|q))*', 'cd', True)
        testDFA('((ab|cd)*|(de*fg|h(ij)*klm*n|q))*', 'dfgab', True)
        testDFA('((ab|cd)*|(de*fg|h(ij)*klm*n|q))*', 'defg', True)
        testDFA('((ab|cd)*|(de*fg|h(ij)*klm*n|q))*', 'deeefg', True)
        testDFA('((ab|cd)*|(de*fg|h(ij)*klm*n|q))*', 'hkln', True)
        testDFA('((ab|cd)*|(de*fg|h(ij)*klm*n|q))*', 'q', True)
        testDFA('((ab|cd)*|(de*fg|h(ij)*klm*n|q))*', 'hijijkln', True)
        testDFA('((ab|cd)*|(de*fg|h(ij)*klm*n|q))*', 'hijijklmmmmmmmmmmn', True)
        testDFA('a*b', 'aaab', True)
        testDFA('ba*', 'baaa', True)
        testDFA('aa|ab|ba|bb', 'aa', True)
        testDFA('(ab|c)*', 'abc', True)
        print("")
        print("---------------------------------------")
        print("")
        print("-----------NFA To DFA---------------")
        showNFAToDFA('a|b')
        showNFAToDFA('a*')
        showNFAToDFA('(ab)*')

        print("")
        print("-----------Equivalence---------------")
        testEquivalence('(a*|b)*b', '(a*|b)*b', True)
        testEquivalence('(a|b|c)*', '(a*b*c*)*', True)
        testEquivalence('(a|b)*c*', '((a*c*)*|(b*c*)*)*', False)
        testEquivalence('(a|b|c)*', '(a|b)*', False)
        testEquivalence('(a|b|c)*', '(a*bab*c*)*', False)

        # print("")
        # print("-----------Wrong Cases---------------")
        # testDFA( '(a*b)*', 'a', False)

    def testunion(strRe, strRe2):
        re = parse_re(strRe)
        nfa1 = re.transformToNFA()

        re2 = parse_re(strRe2)
        nfa2 = re2.transformToNFA()

        dfa1 = nfaToDFA(nfa1)
        dfa2 = nfaToDFA(nfa2)
        print(dfa1.is_accepting)
        dfa1_complement = dfa1.complement()
        dfa2_complement = dfa2.complement()

        statehelper(dfa1)
        print(dfa1.is_accepting)
        statehelper(dfa2)
        print(dfa2.is_accepting)
        statehelper(dfa1_complement)
        print(dfa1_complement.is_accepting)
        statehelper(dfa2_complement)
        print(dfa2_complement.is_accepting)

    # testunion('(a|b)*b', 'a*|bb*a')
    # testunion('(a|b)*b', '(a|b)*b')
    def showNFAToDFA(strRe1):
        re1 = parse_re(strRe1)

        nfa1 = re1.transformToNFA()
        print(strRe1, ": NFA: ")
        statehelper(nfa1)
        print("NFA accepting States are: ", nfa1.accepting)

        dfa1 = nfaToDFA(nfa1)
        print(strRe1, ": DFA: ")
        statehelper(dfa1)
        print("DFA accepting States are: ", dfa1.is_accepting)
        print("")
    
    # test()
    pass
    
