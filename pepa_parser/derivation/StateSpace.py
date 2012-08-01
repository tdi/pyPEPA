#!/usr/bin/env python
from pprint import pprint

class StateSpace():
    operators = []
    components = []
    comp_ss = None

    def __init__(self):
        self.max_length = 0

    def derive(self):
        initial_state = []
        for comp in self.components:
            initial_state.append(comp.name)
        for x in list(range(0,self.max_length+1,1)):
            for op in self.operators:
                if op.length == x:
                    if self.max_length == op.length:
                        new_states = op.compose(self.comp_ss, initial_state, True)
                    else:
                        op.compose(self.comp_ss,initial_state, False)


class Component():
    length = None
    offset = None
    name = None
    ss = None
    data = None


    def __init__(self, ss, name,offset):
        self.name = name
        self.ss = ss
        self.offset = offset
        self.derivatives = []
        for der in self.ss[self.name].transitions:
            self.derivatives.append(Derivative(self.name, [der.to], der.action, der.rate, self.offset))

    def get_derivatives(self):
        return self.derivatives

class Derivative():

    def __init__(self, from_s, to_s, action, rate, offset,shared=False):
        self.from_s = from_s
        self.to_s = to_s
        self.action = action
        self.rate = rate
        self.shared = shared
        self.offset = offset

    def __str__(self):
        return "F:" + self.from_s + " T:" + str(self.to_s) \
                + " Act:"+self.action+" R:"+self.rate+" O:"+str(self.offset)+" Sh:"+str(self.shared)

class Operator(Component):
    length = None
    offset = 0
    actionset = []
    lhs = None
    rhs = None

    def __init__(self):
        self.actionset = []
        self.derivatives = []

    def get_derivatives(self):
        return self.derivatives

    def compose(self,ss, state, topop=False):
        print("OPER" + str(self.actionset))
        print(self.length)
        for tran_l in self.lhs.get_derivatives():
            # UNSHARED
            if tran_l.action not in self.actionset:
                self.derivatives.append(tran_l)
                new_state = state[:]
                new_state[tran_l.offset] = tran_l.to_s[0]
                print("\t/ "+str(tran_l))
        #        print("\tPS "+str(new_state))
            else:
                for tran_r in self.rhs.get_derivatives():
                    if tran_r.action == tran_l.action:
                        new_state = state[:]
                        new_state[tran_r.offset] = tran_r.to_s[0]
                        new_state[tran_l.offset] = tran_l.to_s[0]
                        ddd = Derivative(tran_l.from_s, new_state,tran_l.action,tran_l.rate,self.offset,True)
                        #self.derivatives.append(tran_r)
                        self.derivatives.append(ddd)
                        print("\t |" + str( ddd ))
         #               print("\t PS" + str( new_state ))
        for tran_r in self.rhs.get_derivatives():
            if tran_r.action not in self.actionset:
                self.derivatives.append(tran_r)
                new_state = state[:]
                new_state[tran_r.offset] = tran_r.to_s[0]
                print("\t \\"+str(tran_r))
          #      print("\t PS "+str(new_state))
#            return self.derivatives
#            for _ in self.derivatives:
#                print(_)




