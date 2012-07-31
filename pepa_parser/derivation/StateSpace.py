#!/usr/bin/env python

from pprint import pprint


class StateSpace():
    operators = []
    components = []
    comp_ss = None

    def __init__(self):
        self.max_length = 0

    def derive(self):
        for x in list(range(0,self.max_length+1,1)):
            for op in self.operators:
                if op.length == x:
                    op.compose(self.comp_ss)



    def _components_derivatives(self):
        pass


class Component():
    length = None
    offset = None
    name = None
    derivatives = []


    def __init__(self, ss):
        self.derivatives = ss[self,name].transitions

    def get_derivatives(self):
        return self.derivatives

class Operator(Component):
    length = None
    offset = 0
    actionset = []
    lhs = None
    rhs = None

    def __init__(self):
        self.actionset = []

    def get_derivatives(self,ss):
        return self.derivatives

    def compose(self,ss):
        print("OPER" + str(self.actionset))
        for tran_l in self.lhs.get_derivatives(ss):
            if tran_l.action not in self.actionset:
#                self.derivatives.append(tran_l)
                print("\tLeft " + tran_l.to)
            else:
                for tran_r in self.rhs.get_derivatives(ss):
                    if tran_r.action == tran_l.action:
                        print("\tShared" + tran_r.action + " and " + tran_l.action)
        for tran_r in self.rhs.get_derivatives(ss):
            if tran_r.action not in self.actionset:
#                self.derivatives.append(tran_r)
                print("\tRight " + tran_r.to)


